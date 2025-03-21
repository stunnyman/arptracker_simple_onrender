from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
import plotly.graph_objs as go
from ..database.db import get_latest_arp_values
from ..config.settings import DATABASE_URL

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_root():
    if not DATABASE_URL:
        return HTMLResponse(content="Database not configured")

    rows = await get_latest_arp_values()
    
    if not rows:
        return HTMLResponse(content="No data found")

    timestamps = [row["timestamp"] for row in rows]
    values = [float(row["arp_value"]) for row in rows]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=values, mode='lines+markers', name='ARP Value'))
    fig.update_layout(
        title='ARP for USDT at Binance',
        xaxis_title='Time',
        yaxis_title='%',
        height=600,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    graph_html = fig.to_html(full_html=False)
    html_content = f"""
    <html>
        <head>
            <title>ARP Tracker</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                h1 {{ color: #333; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Binance USDT ARP Tracker</h1>
                {graph_html}
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content) 