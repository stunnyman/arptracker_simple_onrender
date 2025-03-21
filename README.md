# ARP Tracker
- https://arptracker-simple-onrender.onrender.com
- A Python application that tracks and visualizes Annual Return Percentage (ARP) for USDT on Binance.

## Features

- Fetches ARP data from Binance API
- Displays data in an interactive chart
- Optimized for low-resource environments

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following settings:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1`
   - Environment Variables:
     - `DATABASE_URL`: Your PostgreSQL database URL
     - `PYTHON_VERSION`: 3.11.0

### Resource Optimization Tips

1. **Database Optimization**:
   - Use Render's PostgreSQL service!
   - Set up connection pooling (already implemented in the code)
   - Limit query results to 100 records[Optional]

2. **Application Optimization**:
   - Single worker process (--workers 1)
   - Efficient background task scheduling
   - Optimized chart rendering
   - Minimal dependencies

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   echo "DATABASE_URL=your_database_url" > .env
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Database Schema

The application uses a PostgreSQL database with the following table:

```sql
CREATE TABLE arp_values (
    id SERIAL PRIMARY KEY,
    exchange_name VARCHAR(50),
    token VARCHAR(50),
    arp_value DECIMAL,
    timestamp TIMESTAMP
);
```