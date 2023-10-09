# edt challenge

A simple web app API for CRUD operations on a simple DB and an endopoint to send a lat, long and radius to get the total of restaurants, the rate average and the standrad derivation of the ratings.

the end point: /restaurants/statistics?latitude=x&longitude=y&radius=z

Reuqeriments:
 - >= Python3.8 
 - 
Python libs: 
 - fastapi
 - psycopg2
 - sqlalchemy
 - config
 - uvicorn[standrd]

A post man collection is on tests folder to test all the API methods.