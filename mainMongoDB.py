from pymongo import MongoClient
import sys

try:

    def connect_to_mongodb():
        client = MongoClient('mongodb://localhost:27017/')
        return client

    def createDocument(collection, document):
        result = collection.insert_one(document)
        print("Document created with ID:", result.inserted_id)

    def principal():
        client = connect_to_mongodb()
        db = client['prodMongoDictionary']
        collection = db['myDictionary']

        menu = """
    \n__________________________________________
            DICCIONARIO DE SLANG PANAMEÑO
    a) Agregar nueva palabra
    b) Editar palabra existente
    c) Eliminar palabra existente
    d) Ver listado de palabras
    e) Buscar significado de palabra
    f) Salir
    __________________________________________
    Selecciona una opción: """

        option = ""
        while option != "f":
            option = input(menu).lower()
            if option == "a":
                word = input("Ingresa la palabra: ")
                # Comprobar si la palabra ya existe
                possible_meaning = get_meaning(collection, word)
                if possible_meaning:
                    print(f"La palabra '{word}' ya existe")
                # Si no existe:
                else:
                    meaning = input("Ingresa el significado: ")
                    add_word(collection, word, meaning)
                    print(f"Palabra agregada: {word}")
            if option == "b":
                word = input("Ingresa la palabra que quieres editar: ")
                new_meaning = input("Ingresa el nuevo significado: ")
                edit_word(collection, word, new_meaning)
                print(f"Palabra actualizada: {word}")
            if option == "c":
                word = input("Ingresa la palabra a eliminar: ")
                remove_word(collection, word)
                print(f"Palabra eliminada: {word}")
            if option == "d":
                words = get_words(collection)
                print("=== Lista de palabras ===")
                for word in words:
                    # Al leer desde la base de datos se devuelven los datos como arreglo, por lo que hay que imprimir el primer elemento
                    print(word)
            if option == "e":
                word = input("Ingresa la palabra de la cual quieres saber el significado: ")
                meaning = get_meaning(collection, word)
                if meaning:
                    print(f"El significado de '{word}' es: {meaning}")
                else:
                    print(f"Palabra '{word}' no encontrada")
        else:
            print("\nEl programa ha finalizado")
            sys.exit()

    #MÉTODO PARA CREAR DOC

    def create_document(collection, document):
        result = collection.insert_one(document)
        print("Document created with ID:", result.inserted_id)

    #MÉTODO PARA AGREGAR PALABRA
    def add_word(collection, word, meaning):
        document = {"word": word, "meaning": meaning}
        create_document(collection, document)

    #MÉTODO PARA EDITAR PALABRA
    def edit_word(collection, word, new_meaning):
        query = {"word": word}
        new_values = {"$set": {"meaning": new_meaning}}
        result = collection.update_one(query, new_values)
        print(result.modified_count, "documents updated.")

    #MÉTODO PARA ELIMINAR PALABRA
    def remove_word(collection, word):
        query = {"word": word}
        result = collection.delete_one(query)
        print(result.deleted_count, "documents deleted.")

    #MÉTODO PARA OBTENER PALABRAS
    def get_words(collection):
        cursor = collection.find({}, {"word": 1, "_id": 0})
        return [doc["word"] for doc in cursor]

    #MÉTODO PARA OBTENER SIGNIFICADO DE UNA PALABRA   
    def get_meaning(collection, word):
        query = {"word": word}
        document = collection.find_one(query, {"meaning": 1, "_id": 0})
        if document is not None:
            return document.get("meaning")
        else:
            return None

    #GARANTIZAR QUE LA FUNCIÓN 'principal' SOLO SE EJECUTE CUANDO EL ARCHIVO SE EJECUTA COMO PROGRAMA PRINCIPAL Y NO CUANDO SE IMPORTA COMO MÓDULO
    if __name__ == '__main__':
        principal()

#MANEJO DE EXCEPCIONES
except ValueError:
    print("ExceptionError - ValueError: Database not connected")

except TypeError:
    print("ExceptionError - TypeError: Database not connected")

except TimeoutError:
    print("ExceptionError - Timeout: Database not connected")

finally:
    # CIERRE DE CONEXION A BASE DE DATOS SQLITE
    connection = connect_to_mongodb()
    connect_to_mongodb().close