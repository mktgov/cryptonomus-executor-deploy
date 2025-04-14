from omega_executor import webhook_handler

if __name__ == "__main__":
    webhook_handler.app.run(host="0.0.0.0", port=8080)
