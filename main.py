from douglasBlog import app

if __name__ == "__main__":
    # Debug em dev local:
    app.run(host="0.0.0.0", port=5000, debug=True)
    # Produção:
    # app.run(debug=False)
