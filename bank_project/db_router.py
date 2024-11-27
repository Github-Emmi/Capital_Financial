# '''
# I implement a database router that tells Django which database to use for reads 
# and writes for each app.
# '''

# class AppDatabaseRouter:  
#     """  
#     A database router to control all database operations  
#     on models in the venexapp and accounts applications.  
#     """  

#     def db_for_read(self, model, **hints):  
#         if model._meta.app_label == 'venexapp':  
#             return 'venexapp_db'  
#         elif model._meta.app_label == 'accounts':  
#             return 'accounts_db'  
#         return None  

#     def db_for_write(self, model, **hints):  
#         if model._meta.app_label == 'venexapp':  
#             return 'venexapp_db'  
#         elif model._meta.app_label == 'accounts':  
#             return 'accounts_db'  
#         return None  

#     def allow_relation(self, obj1, obj2, **hints):  
#         return True  

#     def allow_migrate(self, db, app_label, model_name=None, **hints):  
#         if app_label == 'venexapp':  
#             return db == 'venexapp_db'  
#         elif app_label == 'accounts':  
#             return db == 'accounts_db'  
#         return db == 'default'