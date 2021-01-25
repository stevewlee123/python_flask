import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel

class Item(Resource):

    parser=reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank!"
            )

    parser.add_argument('store_id',
            type=int,
            required=True,
            help="Every item needs a store id."
            )


    @jwt_required()
    def get (self,name):

        item=ItemModel.find_by_name(name)
        if item:
            return item.json()
        # item=next(filter(lambda x : x['name']==name, items),None)
        return {'message':'Item not found'},404


    def post(self,name):
        
        if ItemModel.find_by_name(name):
            return {'message':"Item {} is exisited".format(name)},400


        data=Item.parser.parse_args()

        # data = request.get_json()

        item=ItemModel(name,**data)


        try:
            item.save_to_db()
        except:
            return {'message':'An error inserting the item.'},500  # internal server error

        return item.json(), 201

    
    def delete(self,name):
        # connection=sqlite3.connect('data.db')
        # cursor=connection.cursor()

        # query="DELETE  FROM items WHERE name =?"

        # result=cursor.execute(query,(name,))

        # connection.commit()
        # connection.close()


        # return {"message":"item deleted."}
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message":"item deleted."}




    def put(self,name):

        data=Item.parser.parse_args()

        item=ItemModel.find_by_name(name)

        # update_item=ItemModel(name,data['price'])

        if item is None:
            # try:
            #     update_item.insert()
            # except:
            #     return {'message':'An error inserting the item.'},500 

            item=ItemModel(name,**data)
        else:
            # try:
            #     update_item.update()
            # except:
            #     return {'message':'An error updating the item.'},500 
            item.price=data['price']

        item.save_to_db()

        return item.json()



class ItemList(Resource):

    def get(self):

        # connection=sqlite3.connect('data.db')
        # cursor=connection.cursor()

        # query="SELECT * FROM items"

        # result=cursor.execute(query)

        # items=[]
        # for row in result:
        #     items.append({'name':row[1],'price':row[2]})

        # connection.close()

        return {'items': [item.json() for item in ItemModel.query.all()]}
