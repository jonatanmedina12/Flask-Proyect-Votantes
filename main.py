from App import create_app,Config

if __name__ == '__main__':
    app = create_app()
    print(Config.HOST)
    app.run(host=Config.HOST, port=Config.PORT)
