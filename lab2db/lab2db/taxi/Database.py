import MySQLdb as mdb
import csv
from xml.dom import minidom


class DB(object):
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection is not None:
            return
        try:
            self.connection = mdb.connect('localhost', 'root', 'pass', 'mydb')

        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            self.connection = None

    def close(self):
        if self.connection is not None:
            self.connection.close()
        self.connection = None

    def initialization(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)

        cur.execute("DELETE FROM taxi_order")

        cur.execute("DELETE FROM address")
        cur.execute("ALTER TABLE address AUTO_INCREMENT = 1")
        cur.execute("commit")

        cur.execute("DELETE FROM car")
        cur.execute("ALTER TABLE car AUTO_INCREMENT = 1")
        cur.execute("commit")

        cur.execute("DELETE FROM client")
        cur.execute("ALTER TABLE client AUTO_INCREMENT = 1")
        cur.execute("commit")

        cur.execute("DELETE FROM taxi_order")
        cur.execute("ALTER TABLE taxi_order AUTO_INCREMENT = 1")
        cur.execute("commit")

        xmldoc = minidom.parse('tables.xml')

        driver_list = xmldoc.getElementsByTagName('driver')
        for driver in driver_list:
            name = str(driver.getElementsByTagName('name')[0].firstChild.data)
            phone = str(driver.getElementsByTagName('phone')[0].firstChild.data)
            cur.execute("INSERT INTO car (driver_name, phone_num) VALUES (%s, %s)", (name, phone))
            cur.execute("commit")

        client_list = xmldoc.getElementsByTagName('client')
        for client in client_list:
            name = str(client.getElementsByTagName('name')[0].firstChild.data)
            phone = str(client.getElementsByTagName('phone')[0].firstChild.data)
            cur.execute("INSERT INTO client(client_name, client_phone) VALUES (%s, %s)", (name, phone))
            cur.execute("commit")

        address_list = xmldoc.getElementsByTagName('address')
        for address in address_list:
            name = str(address.getElementsByTagName('name')[0].firstChild.data)
            x = str(address.getElementsByTagName('x')[0].firstChild.data)
            y = str(address.getElementsByTagName('y')[0].firstChild.data)
            cur.execute("INSERT INTO address(address_name, address_x, address_y) VALUES (%s, %s, %s)", (name, x, y))
            cur.execute("commit")

        order_list = xmldoc.getElementsByTagName('order')
        for order in order_list:
            start_id = str(order.getElementsByTagName('start_id')[0].firstChild.data)
            finish_id = str(order.getElementsByTagName('finish_id')[0].firstChild.data)
            car_id = str(order.getElementsByTagName('car_id')[0].firstChild.data)
            client_id = str(order.getElementsByTagName('client_id')[0].firstChild.data)
            date = str(order.getElementsByTagName('date')[0].firstChild.data)
            cur.execute("INSERT INTO taxi_order (start_id, finish_id, car_id, client_id, data)"
                        " VALUES('%s', '%s', '%s', '%s', '%s')" % (start_id, finish_id, car_id, client_id, date))
            cur.execute("commit")
        self.close()

    def getOrderList(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "select taxi_order.id, car.driver_name, car.phone_num,"
            " client.client_name, client.client_phone,"
            " a1.address_name as start_name, a1.address_x as start_x, a1.address_y as start_y,"
            " a2.address_name as finish_name, a2.address_x as finish_x, a2.address_y as finish_y,"
            " data, 8*((abs(a2.address_y - a1.address_y) + abs(a2.address_x - a1.address_x))) as total"
            " from taxi_order, address as a1, address as a2, car, client"
            " where"
            " car.id = taxi_order.car_id"
            " and client.id = taxi_order.client_id"
            " and taxi_order.start_id = a1.id"
            " and taxi_order.finish_id = a2.id")
        self.close()
        return cur.fetchall()

    def getOrder(self, id):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "select taxi_order.car_id, taxi_order.start_id, taxi_order.client_id,"
            " taxi_order.finish_id, taxi_order.id, car.driver_name, car.phone_num,"
            " client.client_name, client.client_phone,"
            " a1.address_name as start_name, a1.address_x as start_x, a1.address_y as start_y,"
            " a2.address_name as finish_name, a2.address_x as finish_x, a2.address_y as finish_y,"
            " data, 8*((abs(a2.address_y - a1.address_y) + abs(a2.address_x - a1.address_x))) as total"
            " from taxi_order, address as a1, address as a2, car, client"
            " where"
            " car.id = taxi_order.car_id"
            " and client.id = taxi_order.client_id"
            " and taxi_order.start_id = a1.id"
            " and taxi_order.finish_id = a2.id"
            " and taxi_order.id=%d" % int(id))
        self.close()
        return cur.fetchone()

    def getCarList(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "SELECT * FROM car")
        self.close()
        return cur.fetchall()

    def getClientList(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "SELECT * FROM client")
        self.close()
        return cur.fetchall()

    def getAddressList(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "SELECT * FROM address")
        self.close()
        return cur.fetchall()

    def saveOrder(self, startId, finishId, carId, clientId, data):
        self.connect()
        if self.connection is None:
            return []
        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("INSERT INTO taxi_order (start_id, finish_id, car_id, client_id, data)"
                    " VALUES('%s', '%s', '%s', '%s', '%s')" %
                    (int(startId), int(finishId), int(carId), int(clientId), data))
        cur.execute("commit")
        self.close()

    def updateOrder(self, orderId, startId, finishId, carId, clientId, data):
        self.connect()
        if self.connection is None:
            return []
        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("UPDATE taxi_order SET start_id='%s', finish_id='%s', "
                    "car_id='%s', client_id='%s', data='%s' where id=%d" %
                    (int(startId), int(finishId), int(carId), int(clientId), data, int(orderId)))
        cur.execute("commit")
        self.close()

    def removeOrder(self, id):
        self.connect()
        if self.connection is None:
            return []
        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("DELETE FROM taxi_order WHERE id = '%d' " % (int(id)))
        cur.execute("commit")
        self.close()

    def getOrderListByLength(self, fromLength, toLenght):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "select taxi_order.id, car.driver_name, car.phone_num,"
            " client.client_name, client.client_phone,"
            " a1.address_name as start_name, a1.address_x as start_x, a1.address_y as start_y,"
            " a2.address_name as finish_name, a2.address_x as finish_x, a2.address_y as finish_y,"
            " data, (8*((abs(a2.address_y - a1.address_y) + abs(a2.address_x - a1.address_x)))) as total"
            " from taxi_order, address as a1, address as a2, car, client"
            " where"
            " taxi_order.car_id = car.id"
            " and taxi_order.client_id = client.id"
            " and taxi_order.start_id = a1.id"
            " and taxi_order.finish_id = a2.id"
            " and (8*((abs(a2.address_y - a1.address_y) + abs(a2.address_x - a1.address_x)))) BETWEEN '%s'  AND  '%s'"
            % (fromLength, toLenght))
        self.close()
        return cur.fetchall()

    def getOrderListByDriverID(self, car_id):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "select taxi_order.id, car.driver_name, car.phone_num,"
            " client.client_name, client.client_phone,"
            " a1.address_name as start_name, a1.address_x as start_x, a1.address_y as start_y,"
            " a2.address_name as finish_name, a2.address_x as finish_x, a2.address_y as finish_y,"
            " data, (8*((abs(a2.address_y - a1.address_y) + abs(a2.address_x - a1.address_x)))) as total"
            " from taxi_order, address as a1, address as a2, car, client"
            " where"
            " taxi_order.car_id = car.id"
            " and taxi_order.client_id = client.id"
            " and taxi_order.start_id = a1.id"
            " and taxi_order.finish_id = a2.id"
            " and car.id = '%s' " % car_id)
        self.close()
        return cur.fetchall()

    def getListExcluded(self, phrase):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute(
            "select taxi_order.car_id, taxi_order.start_id, taxi_order.client_id,"
            " taxi_order.finish_id, taxi_order.id, car.driver_name, car.phone_num,"
            " client.client_name, client.client_phone,"
            " a1.address_name as start_name, a1.address_x as start_x, a1.address_y as start_y,"
            " a2.address_name as finish_name, a2.address_x as finish_x, a2.address_y as finish_y,"
            " data, 8*((abs(a2.address_y - a1.address_y) + abs(a2.address_x - a1.address_x))) as total"
            " from taxi_order, address as a1, address as a2, car, client"
            " where"
            " taxi_order.car_id = car.id"
            " and taxi_order.client_id = client.id"
            " and taxi_order.start_id = a1.id"
            " and taxi_order.finish_id = a2.id"
            " and (MATCH (car.driver_name) AGAINST ('\"%s\"' IN BOOLEAN MODE))" % phrase)
        self.close()
        return cur.fetchall()

    def getListIncluded(self, phrase):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        newphrase = ""
        for str in phrase.split(" "):
            newphrase = newphrase + " +" + str
            print newphrase

        cur.execute(
            "select taxi_order.car_id, taxi_order.start_id, taxi_order.client_id,"
            " taxi_order.finish_id, taxi_order.id, car.driver_name, car.phone_num,"
            " client.client_name, client.client_phone,"
            " a1.address_name as start_name, a1.address_x as start_x, a1.address_y as start_y,"
            " a2.address_name as finish_name, a2.address_x as finish_x, a2.address_y as finish_y,"
            " data, 8*((abs(a2.address_y - a1.address_y) + abs(a2.address_x - a1.address_x))) as total"
            " from taxi_order, address as a1, address as a2, car, client"
            " where"
            " taxi_order.car_id = car.id"
            " and taxi_order.client_id = client.id"
            " and taxi_order.start_id = a1.id"
            " and taxi_order.finish_id = a2.id"
            " and (MATCH (car.driver_name) AGAINST ('%s' IN BOOLEAN MODE))" % newphrase)
        self.close()
        return cur.fetchall()
