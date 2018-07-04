import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from catordog import CatOrDog
from flask import render_template
from os.path import basename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.catordog = CatOrDog()   

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    #string de HTML
    first=""
    second=""
    third=""
    htmlpic=""
    maxPrice=""
    minPrice=""
    meanPrice=""
    image=""
    product=""
    secMax=""
    secMin=""
    secMean=""
    trdMax=""
    trdMin=""
    trdMean=""
    from os import listdir
    from os.path import isfile, join
    import pandas as pd
    if request.method == 'POST':
        import time
        start_time = time.time()
        file = request.files['file']
        #Guarda la imagen y recarga la pagina
        if file and allowed_file(file.filename):
            #Remover archivos anteriores para usar solo la más reciente
            for f in listdir(UPLOAD_FOLDER):
                if isfile(join(UPLOAD_FOLDER,f)) and f != '.gitignore':
                    print(f)
                    os.remove(join(UPLOAD_FOLDER,f))
            filename = secure_filename(file.filename)
            #Folder donde se guardará la imágen
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #Guardar la imágen
            file.save(file_path)
            #Imprimir el la consola
            print("--- %s seconds ---" % str (time.time() - start_time))
            #Recorrer el folder
            for f in listdir(UPLOAD_FOLDER):
                #Revisar todo menos el .gitgnore
                if isfile(join(UPLOAD_FOLDER,f)) and f != '.gitignore':
                    print(f)
                    fst,sec,trd = app.catordog.run('uploads/'+f)
                    first+=fst  
                    second+=sec
                    third+=trd
                    #Leer el CSV con el nombre clasificado
                    df=pd.read_csv('csv/'+first+'.csv', sep=',' )
                    df.values
                    maxPrice=str(df['price'].max())
                    minPrice+=str(df['price'].min())
                    meanPrice+=str(df['price'].mean())
                    image=f
                    product+=first

                    df2=pd.read_csv('csv/'+second+'.csv', sep=',' )
                    df2.values 
                    df3=pd.read_csv('csv/'+third+'.csv', sep=',' )
                    df3.values
                    secMax+=str(df2['price'].max())
                    secMin+=str(df2['price'].min())
                    secMean+=str(df2['price'].mean())

                    trdMax+=str(df3['price'].max())
                    trdMin+=str(df3['price'].min())
                    trdMean+=str(df3['price'].mean())
            return render_template("index.html", img=image, product=product, maxP=maxPrice, minP=minPrice, meanP=meanPrice, secName=second,trdName=third,secMax=secMax,secMin=secMin,secMean=secMean,trdMax=trdMax,trdMin=trdMin,trdMean=trdMean)
    
    
            #Agregar la imagen, clasificacion y precios al HTML
            #htmlpic += "<p style='text-transform: uppercase; font-weight: bolder'>" + f.split('__')[0] +"</p><p> <strong>Menor precio: </strong>"+ str(df['price'].min()) +"</p><p> <strong>Mayor precio:</strong> "+ str(df['price'].max()) +"</p><p> <strong>Precio promedio:</strong> "+ str(df['price'].mean())  + "</p><img width=300px height=250px src='uploads/"+f +"'>"
    
    #Devolver el html
    #Remover archivos anteriores para usar solo la más reciente
    for f in listdir(UPLOAD_FOLDER):
        if isfile(join(UPLOAD_FOLDER,f)) and f != '.gitignore':
            print(f)
            os.remove(join(UPLOAD_FOLDER,f))
    return render_template("uploads.html")
#"""
#    <!doctype html>
#    <head>
#    <title>Clasificador</title>
#    </head>
#   <body>
#    <h1 style='text-transform: uppercase; font-weight: bolder'>Subir foto</h1>
#    <form action='' method=post enctype=multipart/form-data>
#      <p><input type=file name=file>
#         <input type=submit value=Upload>
#    </form>
#    """+htmlpic+"""
#    </body>
#    """


@app.route('/uploads/<filename>')

def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

from werkzeug import SharedDataMiddleware
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0', port=8000)
