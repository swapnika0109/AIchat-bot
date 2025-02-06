from visualization.dashboard import Dashboard

def main():
    print("Starting application...")
    dashboard = Dashboard()
    print("Running dashboard...")
    dashboard.run_server(debug=True, port=8501)

if __name__ == "__main__":
    main() 