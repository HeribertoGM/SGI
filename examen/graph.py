from sqlalchemy import create_engine, select, MetaData
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def main():
    # Conexión a la base de datos
    engine = create_engine('postgresql+psycopg2://usr:pword@localhost/MemSch')
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Cargar datos
    mda = pd.read_sql(select(metadata.tables['memtramdadet']).select_from(metadata.tables['memtramdadet']), engine)
    mtr = pd.read_sql(select(metadata.tables['memtramtrdet']).select_from(metadata.tables['memtramtrdet']), engine)
    tc = pd.read_sql(select(metadata.tables['memtratcdet']), engine)
    tbfin = pd.read_sql(select(metadata.tables['memtratbfin']), engine)

    mda_01ans85 = mda[mda['clanodo'] == '01ANS-85']
    mda_01ans85['datetime'] = pd.to_datetime(mda_01ans85['fecha']) + pd.to_timedelta(mda_01ans85['hora'], unit='h')
    mtr_01ans85 = mtr[mtr['clanodo'] == '01ANS-85']
    mtr_01ans85['datetime'] = pd.to_datetime(mtr_01ans85['fecha']) + pd.to_timedelta(mtr_01ans85['hora'], unit='h')
    
    # Gráfica evolución del precio MDA y MTR para nodo 01ANS-85
    fig, ax = plt.subplots()
    ax.plot(mda_01ans85['datetime'], mda_01ans85['pml'], label="MDA")
    ax.plot(mtr_01ans85['datetime'], mtr_01ans85['pml'], label="MTR")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig.autofmt_xdate()
    plt.title('Evolución del precio MDA y MTR para nodo 01ANS-85')
    plt.xlabel('Fecha y Hora')
    plt.ylabel('Precio')
    plt.show()

    # Diferencia promedio diaria entre MDA y MTR
    fig, ax = plt.subplots()
    mda_prices = mda.groupby('fecha')['pml'].mean()
    mtr_prices = mtr.groupby('fecha')['pml'].mean()
    diff_avg = abs(mda_prices - mtr_prices).reset_index(name='diff_avg')
    ax.plot(diff_avg['fecha'], diff_avg['diff_avg'])
    fig.autofmt_xdate()
    plt.title(('Diferencia (absoluta) Promedio MDA vs MTR'))
    plt.xlabel('Fecha')
    plt.ylabel('| MDA - MTR |')
    plt.show()

    # Unir MDA y MTR
    mda['origen'] = 'MDA'
    mtr['origen'] = 'MTR'
    mda_mtr = pd.concat([mda, mtr], ignore_index=True)

    # Unir con TC
    merged = pd.merge(mda_mtr, tc, on='fecha', how='left', suffixes=('', '_tc'))
    
    # DataFrame Nodo, fecha, hora, pml, tbfin con pml > tbfin
    filtered = pd.merge(merged, tbfin, on='fecha', how='left')
    filtered = filtered[filtered['pml'] > filtered['tbfin']][['clanodo', 'fecha', 'hora', 'pml', 'tbfin']]

    # DataFrame promedio diario de los precios del pml
    daily_avg_pml = merged.groupby('fecha')['pml'].mean().reset_index()

    # Gráfica del Nodo y TbFin por fecha y hora
    for nodo in filtered['clanodo'].unique():
        nodo_data = filtered[filtered['clanodo'] == nodo]
        plt.plot(nodo_data['hora'], nodo_data['pml'], label=f'{nodo} PML')
        plt.plot(nodo_data['hora'], nodo_data['tbfin'], label=f'{nodo} tbfin', linestyle='--')
        plt.title(f'Precio PML vs TbFin para Nodo {nodo}')
        plt.xlabel('Hora')
        plt.ylabel('Precio')
        plt.legend()
        plt.show()

    engine.dispose()

if __name__ == "__main__":
    main()