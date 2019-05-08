import sqlite3
import json
import re
import numpy as np
import requests
import os
from imageio import imread, imsave
from PIL import Image
import numpy as np
import random
import string
import decimal
from datetime import timedelta, datetime


def parse_data(dic):
    dic['SALE_PRICE'] = float(
        np.mean([float(i) for i in re.findall(r'\d+.?\d+', str(dic['SALE_PRICE']).replace(',', ''))]))
    dic['ORIGINAL_PRICE'] = float(
        np.mean([float(i) for i in re.findall(r'\d+.?\d+', str(dic['ORIGINAL_PRICE']).replace(',', ''))]))
    dic['CTYPE'] = re.split(r'\s+\>\s+', str(dic['CTYPE']))[-1]
    dic['CLOSED'] = 0
    if not os.path.exists(os.path.join('../media/images', dic['IMAGE'].split('/')[-1]).replace('jpg', 'png')):
        print(dic['IMAGE'])
        with open(os.path.join('../media/images', dic['IMAGE'].split('/')[-1]), 'wb') as f:
            img = requests.get(dic['IMAGE'])
            f.write(img.content)
    dic['IMAGE'] = os.path.join('images', dic['IMAGE'].split('/')[-1])
    dic['DETAIL'] = dic['DETAIL'].split('; ')
    summ_len = 0
    res_det = []
    for det in dic['DETAIL']:
        if summ_len + len(det) < 200:
            summ_len += len(det)
            res_det.append(det)
    dic['DETAIL'] = '; '.join(res_det)
    result_lst = [
        dic['ORIGINAL_PRICE'],
        dic['SALE_PRICE'],
        dic['CONDITION'],
        dic['SIZE'],
        dic['COLOR'],
        dic['BRAND'],
        dic['CTYPE'],
        dic['CLOSED'],
        dic['DETAIL'],
        dic['IMAGE']
    ]
    return [str(i) if type(i) not in [int, float, ] else i for i in result_lst]


data = json.loads(open('./data.json').read())
data = [i for i in data if i['IMAGE'] is not None]
parsed = [parse_data(samp) for samp in data]
samp_data = parsed[0]
print('Length of data {}'.format(len(parsed)))
print('Sample date')
print(samp_data)

conn = sqlite3.connect('../db.sqlite3')
c = conn.cursor()

command = '''DELETE FROM fashion_bidding WHERE id > 0'''
c.execute(command)
conn.commit()

command = '''DELETE FROM fashion_clothes WHERE id > 1'''
c.execute(command)
conn.commit()

command = '''DELETE FROM fashion_person WHERE id > 3'''
c.execute(command)
conn.commit()

NUM_USER = 20000
print('Creating {} users'.format(NUM_USER))
for i in range(NUM_USER):
    uid = i + 4
    collegeid = ''.join([str(int(i)) for i in np.random.randint(0, 9, 7)])
    username = ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(np.random.randint(3, 20, 1)[0]))
    if np.random.rand(1)[0] < .85:
        phone = ''.join([str(int(i)) for i in np.random.randint(0, 9, 10)])
    else:
        phone = 'NULL'
    email = ''.join(random.choice(string.digits + string.ascii_letters) for _ in
                    range(np.random.randint(5, 15, 1)[0])) + '@' + random.choice(
        ['gmail.com', 'hotmail.com', 'duke.edu'])
    command = '''INSERT INTO fashion_person VALUES ({}, {}, {}, '{}', {}, {}, '{}')'''.format(uid, collegeid, phone,
                                                                                              email, 0, uid, username)
    c.execute(command)
    conn.commit()

print('Creating clothes')
cho = np.random.choice([i for i in range(len(parsed))], len(parsed), replace=False)
for ind, samp_data in enumerate(parsed):
    open_until = datetime.now() + timedelta(days=random.choice(range(1, 30)),
                                            minutes=random.choice(range(60)),
                                            seconds=random.choice(range(60)),
                                            hours=random.choice(range(24)))
    command = '''INSERT INTO fashion_clothes VALUES ({},{},{},{},'{}','{}','{}','{}','{}',{},'{}','{}','{}')'''.format(
        cho[ind] + 2, random.choice(range(NUM_USER)),
        *tuple([str(i).replace("'", "''") if type(i) == str else i for i in samp_data]),
        open_until.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        c.execute(command)
        conn.commit()
    except Exception as e:
        print(e)
        print(command)

for ind, samp_data in enumerate(parsed):
    command = '''UPDATE fashion_clothes SET image='{}' WHERE id = {}'''.format(samp_data[-1], cho[ind] + 2)
    try:
        c.execute(command)
        conn.commit()

    except Exception as e:
        print(e)
        print(command)

c.execute("SELECT * FROM fashion_clothes")
for i in c.fetchall():
    c.execute("UPDATE fashion_clothes SET image='{}' WHERE id = {}".format(i[-2].replace('jpg', 'png'), i[0]))
    conn.commit()

c.execute("SELECT * FROM fashion_clothes")
for i in c.fetchall():
    c.execute("UPDATE fashion_clothes SET sellprice={} WHERE id = {}".format(
        round(i[2] * (1 - float(decimal.Decimal(random.randrange(0, 95)) / 100)), 1) + .09, i[0]))
    conn.commit()

print('Creating bidding')
c.execute("SELECT id, sellerid_id, sellprice FROM fashion_clothes")
all_clothes = c.fetchall()
cnt = 0
for i, (cid, sid, price) in enumerate(all_clothes):
    num_bidding = random.choice(range(5, 10))
    new_prices = sorted([np.round(np.random.rand(1)[0] * .25 * price + price, 2) for i in range(num_bidding)])
    rand_ds = sorted([datetime.now() - timedelta(days=random.choice(range(7)),
                                                 minutes=random.choice(range(60)),
                                                 seconds=random.choice(range(60)),
                                                 hours=random.choice(range(24))) for i in range(num_bidding)])
    for new_price, rand_d in zip(new_prices, rand_ds):
        for j in range(10):
            new_sid = random.choice(range(10000))
            if new_sid != sid:
                break
        command = '''INSERT INTO fashion_bidding VALUES ({},{},{},{},'{}')'''.format(cnt + 1, new_price, cid, new_sid,
                                                                                     rand_d.strftime(
                                                                                         "%Y-%m-%d %H:%M:%S"
                                                                                     ))
        try:
            c.execute(command)
            cnt += 1
        except Exception as e:
            print(command)
            print(e)
            break
        conn.commit()

conn.close()

print('Convert jpg to png')
for img_name in os.listdir('../media/images/'):
    if 'jpg' not in img_name:
        continue
    print(img_name)
    img = np.array(imread('../media/images/{}'.format(img_name)))
    m, n, c = img.shape
    new_img = np.dstack([img, np.zeros([m, n])])
    for x in range(new_img.shape[0]):
        for y in range(new_img.shape[1]):
            if not any(i == 255 for i in new_img[x, y, :3]):
                new_img[x, y, 3] = 255
    imsave(uri='../media/images/{}'.format(img_name).replace('jpg', 'png'), im=new_img.astype(np.uint8), format='PNG')
    os.remove('../media/images/{}'.format(img_name))
