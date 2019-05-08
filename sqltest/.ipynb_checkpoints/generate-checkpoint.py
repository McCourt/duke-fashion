import numpy as np
import random
import string

NUM_USER = 10000
NUM_BIDDING = 10000

if __name__=='__main__':
    with open('./test-production.sql', 'w') as f:
        f.write('INSERT INTO Person VALUES\n')
        for i in range(NUM_USER):
            uid = i
            collegeid = ''.join([str(int(i)) for i in np.random.randint(0, 9, 7)])
            username = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(np.random.randint(3, 20, 1)[0]))
            if np.random.rand(1)[0] < .5:
                phone = ''.join([str(int(i)) for i in np.random.randint(0, 9, 10)])
            else:
                phone = 'NULL'
            email = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(np.random.randint(5, 15, 1)[0])) + '@' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(np.random.randint(1, 2, 1)[0])) + '.com'
            SHApassword = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(18))
            if i == NUM_USER - 1:
                line = "({}, {}, '{}', {}, '{}', '{}');\n".format(uid, collegeid, username, phone, email, SHApassword)
            else:
                line = "({}, {}, '{}', {}, '{}', '{}'),\n".format(uid, collegeid, username, phone, email, SHApassword)
            f.write(line)
            f.flush()

        f.write('\nINSERT INTO Seller VALUES\n')
        seller_id = np.random.choice([i for i in range(NUM_USER)], size=int(0.2 * NUM_USER), replace=False)
        for ind, i in enumerate(seller_id):
            if ind == len(seller_id) - 1:
                line = '({}, {});\n'.format(i, 0)
            else:
                line = '({}, {}),\n'.format(i, 0)
            f.write(line)
            f.flush()

        f.write('\nINSERT INTO Clothes VALUES\n')
        conditions = ['new', 'nearly new', 'used', 'damaged', 'usable']
        sizes = ['xs', 's', 'm', 'l', 'xl']
        colors = ['red', 'violet', 'blue', 'green']
        brands = ['Armani', 'Adidas', 'Cartier', 'H&M', 'Zara', 'Nike', 'Chanel']
        ctypes = ['coat', 'jacket', 'blazer', 'dress', 'shirts', 'hoody',
                  'blouses', 'tops', 'sweatshirts', 'pants', 'jeans', 'shorts',
                  'skirts', 'suits', 'shoes', 'bags', 'accessories', 'others']
        for ind, i in enumerate([random.choice(seller_id) for _ in range(NUM_BIDDING)]):
            cid = ind
            sellerid = i
            if np.random.rand(1)[0] < .5:
                orginalprice = np.round(np.random.rand(1)[0] * 1e4, 2)
            else:
                orginalprice = 'NULL'
            sellprice = np.round(np.random.rand(1)[0] * 1e4, 2)
            condition = random.choice(conditions)
            size = random.choice(sizes)
            if np.random.rand(1)[0] < .5:
                color = random.choice(colors)
            else:
                color = 'NULL'
            if np.random.rand(1)[0] < .5:
                brand = random.choice(brands)
            else:
                brand = 'NULL'
            if np.random.rand(1)[0] < .5:
                ctype = random.choice(ctypes)
            else:
                ctype = 'NULL'
            if np.random.rand(1)[0] < .5:
                description = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(np.random.randint(5, 50, 1)[0]))
            else:
                description = 'NULL'
            closed = 'FALSE'
            imgpath = 'NULL'
            if ind == NUM_BIDDING - 1:
                line = "({}, {}, {}, {}, '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}');\n".format(cid, sellerid, orginalprice,
                                                            sellprice, condition, size,
                                                            color, brand, ctype, description,
                                                            closed, imgpath)
            else:
                line = "({}, {}, {}, {}, '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}'),\n".format(cid, sellerid, orginalprice,
                                                            sellprice, condition, size,
                                                            color, brand, ctype, description,
                                                            closed, imgpath)
            f.write(line.replace('"NULL"', 'NULL'))
            f.flush()

        f.write('\nSELECT * FROM Bidding;\n')
        f.write('\n')

        for i in np.random.choice([i for i in range(NUM_BIDDING)], size=NUM_BIDDING):
            f.write('UPDATE Bidding SET biddingprice = {} WHERE cid = {};\n'.format(np.round(np.random.rand(1)[0] * 1e4, 2), i))
