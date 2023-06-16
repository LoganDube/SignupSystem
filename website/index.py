from main import create_app

app = create_app()

#running of the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')