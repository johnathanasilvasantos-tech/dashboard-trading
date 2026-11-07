import plotly.graph_objects as go
from config import COR_FUNDO, COR_ALTA

def grafico_linha(df, titulo):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Preço', line=dict(color=COR_ALTA, width=2)))
    fig.update_layout(
        title=titulo,
        paper_bgcolor=COR_FUNDO, plot_bgcolor=COR_FUNDO,
        font=dict(color='white'),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#2A2F45')
    )
    return fig