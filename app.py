from project import app

if os.environ.get('ENV') == 'production':
    debug = False
else:
    debug = True

if __name__ == '__main__':
  app.run(debug=debug, port=3000)
