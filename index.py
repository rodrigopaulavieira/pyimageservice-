import tornado.web
import tornado.ioloop
import os

base_path = os.path.dirname(__file__)
static_path = os.path.join(base_path, "img")


class uploadHandler(tornado.web.RequestHandler):
    def get(self):
            self.render("upload.html")

    def post(self):
 
        file1 = self.request.files['imgFile'][0]
        filename = file1.get('filename')
        body = file1.get('body')

        if not filename or not body:
            self.set_status(400)
            return self.write("Arquivo inválido.")
        
        # caminho seguro relativo ao arquivo Python atual
        base_path = os.path.dirname(__file__)
        save_dir = os.path.join(base_path, "img")   # ou 'uploads'
        os.makedirs(save_dir, exist_ok=True)       # cria a pasta se não existir

        save_path = os.path.join(save_dir, filename)
        
        
         # grava o arquivo em binário
        try:
            with open(save_path, 'wb') as fh:
                fh.write(body)
        except Exception as e:
            self.set_status(500)
            return self.write(f"Erro ao salvar arquivo: {e}")
        
        self.write(f"Image {filename} uploaded successfully! Caminho: {save_path}")



if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", uploadHandler),
        ("/img/(.*)", tornado.web.StaticFileHandler, {"path": static_path})
    ], debug=True)
    app.listen(8080)
    print("Server started at http://localhost:8080")
    print("Serving static files from:", static_path)
    tornado.ioloop.IOLoop.instance().start()