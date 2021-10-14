import streamlit as st
import pandas as pd
import altair as alt



st.set_page_config(
    page_title="Listado de lavadoras",
    )

#st.title('Encuentra la lavadora que mejor se adapte a tus necesidades')
st.markdown("<h1 style='text-align: center; '>Encuentra la lavadora que mejor se adapte a tus necesidades</h1>", unsafe_allow_html=True)


#########
#FUNCIONES

def asignar_punt(divisor, lista, data, iterador, categoria, punt_min):
    puntuacion = round((divisor - lista.index(data.iloc[iterador][categoria])) * punt_min, 1)
    return puntuacion

#########


@st.cache(ttl=300)
def load_data(url):
    df = pd.read_csv(url)
    return df





url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTKAItDsAEOdfD2sdiS3ip5Vm6HDDkHKP3IGlm06P-1Fm4m6D9Yxx91hzJN6hT-SVC-nZT_HhjspSe9/pub?gid=0&single=true&output=csv'
#df = pd.read_csv(url)

df = load_data(url)

df = df.dropna()
df.reset_index(drop=True, inplace=True)

Marca_List = list(df['Marca'].unique())
Marca_List.sort()

Carga_List = list(df['Carga'].unique())
Carga_List.sort()

Capacidad_List = list(df['Capacidad'].unique())
Capacidad_List.sort(reverse=True)

Vel_Cent_List = list(df['Centrifugado'].unique())
Vel_Cent_List.sort(reverse=True)

Con_Ene_List = list(df['Energia'].unique())
Con_Ene_List.sort()

Tiempo_List = list(df['Tiempo'].unique())
Tiempo_List.sort(reverse= False)

Con_Agu_List = list(df['Agua'].unique())
Con_Agu_List.sort(reverse= False)

Ruido_List = list(df['Ruido'].unique())
Ruido_List.sort(reverse= False)

divisor = max(len(Capacidad_List), len(Vel_Cent_List), len(Con_Ene_List), len(Tiempo_List), len(Con_Agu_List), len(Ruido_List))

punt_max = 100
punt_min = 100 / divisor


df['CC'] = [asignar_punt(divisor, Capacidad_List, df, i, 'Capacidad', punt_min) for i in df.index]
df['VC'] = [asignar_punt(divisor, Vel_Cent_List, df, i, 'Centrifugado', punt_min) for i in df.index]
df['CE'] = [asignar_punt(divisor, Con_Ene_List, df, i, 'Energia', punt_min) for i in df.index]
df['TL'] = [asignar_punt(divisor, Tiempo_List, df, i, 'Tiempo', punt_min) for i in df.index]
df['CA'] = [asignar_punt(divisor, Con_Agu_List, df, i, 'Agua', punt_min) for i in df.index]
df['RL'] = [asignar_punt(divisor, Ruido_List, df, i, 'Ruido', punt_min) for i in df.index]
df['PT'] = round((df['CC'] + df['VC'] + df['CE'] + df['TL'] + df['CA'] + df['RL']) / 6, 1)


lista_comp = df[['Capacidad', 'Centrifugado', 'Energia', 'Tiempo', 'Agua', 'Ruido']].columns.tolist()
lista_comp.sort()





col1, col2 = st.columns((2,4))
with col1:
    chosen_TP = st.radio(
    'Tipo de carga',
    (df['Carga'].unique()))
with col2:
    slider_KG = st.slider(
    'Capacidad de lavado (kg)',
    int(Capacidad_List[0]), int(Capacidad_List[-1]), (int(Capacidad_List[0]), int(Capacidad_List[-1]))
)



options_MA = st.multiselect(
    'Marcas',
    Marca_List, Marca_List
)


    

importancia = [10,9,8,7,6,5,4,3,2,1,0]

st.write('¿Qué importancia le das a cada una de estas características?')

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    imp_CC = st.selectbox(
    'Capacidad:',
    (importancia), index=0)

with col2:
    imp_VC = st.selectbox(
    'Centrifugado:',
    (importancia))

with col3:
    imp_CE = st.selectbox(
    'Energia:',
    (importancia), index=0)

with col4:
    imp_TL = st.selectbox(
    'Tiempo:',
    (importancia))

with col5:
    imp_CA = st.selectbox(
    'Agua:',
    (importancia), index=0)

with col6:
    imp_RL = st.selectbox(
    'Ruido:',
    (importancia))


contador_importancia = imp_CC + imp_VC + imp_CE + imp_TL + imp_CA + imp_RL

df['PA'] = (df['CC'] * imp_CC + df['VC'] * imp_VC + df['CE'] * imp_CE + df['TL'] * imp_TL + df['CA'] * imp_CA + df['RL'] * imp_RL) / contador_importancia



a = df[(df['Capacidad'] >= slider_KG[0]) & (df['Capacidad'] <= slider_KG[-1]) & (df['Carga'] == chosen_TP) & (df.Marca.isin(options_MA))]

a.reset_index()





if len(a) == 0:
    st.warning('Revisa los filtros. No hay resultados')
    e = a.sort_values('PA', ascending=False).reset_index()
else:
    e = a.sort_values('PA', ascending=False).reset_index()
    
    
    
    grupo_marcas = pd.DataFrame(e.groupby(['Marca'])['Cod Articulo'].count())
    
    #grupo_marcas.rename(columns={'Cod Articulo':'Lavadoras'}, inplace=True)
        
    grupo_marcas['Capacidad'] = round(pd.DataFrame(e.groupby(['Marca'])['Capacidad'].mean()),1)
    grupo_marcas['Centrifugado'] = round(pd.DataFrame(e.groupby(['Marca'])['Centrifugado'].mean()),1)
    grupo_marcas['Energia'] = round(pd.DataFrame(e.groupby(['Marca'])['Energia'].mean()),1)
    grupo_marcas['Tiempo'] = round(pd.DataFrame(e.groupby(['Marca'])['Tiempo'].mean()),1)
    grupo_marcas['Agua'] = round(pd.DataFrame(e.groupby(['Marca'])['Agua'].mean()),1)
    grupo_marcas['Ruido'] = round(pd.DataFrame(e.groupby(['Marca'])['Ruido'].mean()),1)
    
    grupo_marcas.reset_index(level=0, inplace=True)
    
    grupo_marcas = grupo_marcas.sort_values('Cod Articulo', ascending=False)
    
    
    
    #Puntuaciones
    
    grupo_marcas_punt = pd.DataFrame(e.groupby(['Marca'])['Cod Articulo'].count())
    
    grupo_marcas_punt.rename(columns={'Cod Articulo':'Lavadoras'}, inplace=True)
        
    grupo_marcas_punt['CC'] = round(pd.DataFrame(e.groupby(['Marca'])['CC'].mean()),1)
    grupo_marcas_punt['VC'] = round(pd.DataFrame(e.groupby(['Marca'])['VC'].mean()),1)
    grupo_marcas_punt['CE'] = round(pd.DataFrame(e.groupby(['Marca'])['CE'].mean()),1)
    grupo_marcas_punt['TL'] = round(pd.DataFrame(e.groupby(['Marca'])['TL'].mean()),1)
    grupo_marcas_punt['CA'] = round(pd.DataFrame(e.groupby(['Marca'])['CA'].mean()),1)
    grupo_marcas_punt['RL'] = round(pd.DataFrame(e.groupby(['Marca'])['RL'].mean()),1)
    #grupo_marcas_punt['PT'] = round(pd.DataFrame(e.groupby(['Marca'])['PT'].mean()),1)
    grupo_marcas_punt['PA'] = round(pd.DataFrame(e.groupby(['Marca'])['PA'].mean()),1)
    
    grupo_marcas_punt = grupo_marcas_punt.sort_values('PA', ascending=False)
    


    
    
    contador = 0
    
    
    
    st.markdown("<h1 style='text-align: center; '>TOP mejores lavadoras</h1>", unsafe_allow_html=True)
    
    


    col1, col2, col3 = st.columns(3)
    with col1:
        
        st.subheader(str(contador+1) + ') ' + str(e['Marca'][contador]))
        st.text(str(e['Modelo'][contador]))
        
        st.image(e['Imagen'][contador], use_column_width=True)
        
        
        with st.expander("Ver características"):
        
            st.metric(label="Capacidad", value=str(e['Capacidad'][contador]) + ' kg', delta=str(round(e['Capacidad'][contador]-e['Capacidad'].mean(),2)) + ' kg')
            st.metric(label="Centrifugado", value=str(e['Centrifugado'][contador])+ ' RPM', delta=str(round(e['Centrifugado'][contador]-e['Centrifugado'].mean(),2)) + ' RPM')
            st.metric(label="Energia", value=str(e['Energia'][contador])+ ' kwh', delta=str(round(e['Energia'][contador]-e['Energia'].mean(),2)) + ' kwh', delta_color="inverse")
            st.metric(label="Tiempo", value=str(e['Tiempo'][contador])+ ' min', delta=str(round(e['Tiempo'][contador]-e['Tiempo'].mean(),2)) + ' min', delta_color="inverse")
            st.metric(label="Agua", value=str(e['Agua'][contador])+ ' l', delta=str(round(e['Agua'][contador]-e['Agua'].mean(),2)) + ' l', delta_color="inverse")
            st.metric(label="Ruido", value=str(e['Ruido'][contador])+ ' dB', delta=str(round(e['Ruido'][contador]-e['Ruido'].mean(),2)) + ' dB', delta_color="inverse")
            st.metric(label="Puntuación", value=str(round(e['PA'][contador],1))+ ' p', delta=str(round(e['PA'][contador]-e['PA'].mean(),2)) + ' p')
        
        st.write(str(e['Enlace'][contador]),unsafe_allow_html=True,)
        
        
    if contador + 1 < len(e):
        with col2:
            contador = 1
        
            st.subheader(str(contador+1) + ') ' + str(e['Marca'][contador]))
            st.text(str(e['Modelo'][contador]))
                    
            st.image(e['Imagen'][contador], use_column_width=True)
                    
            with st.expander("Ver características"):
                    
                st.metric(label="Capacidad", value=str(e['Capacidad'][contador]) + ' kg', delta=str(round(e['Capacidad'][contador]-e['Capacidad'].mean(),2)) + ' kg')
                st.metric(label="Centrifugado", value=str(e['Centrifugado'][contador])+ ' RPM', delta=str(round(e['Centrifugado'][contador]-e['Centrifugado'].mean(),2)) + ' RPM')
                st.metric(label="Energia", value=str(e['Energia'][contador])+ ' kwh', delta=str(round(e['Energia'][contador]-e['Energia'].mean(),2)) + ' kwh', delta_color="inverse")
                st.metric(label="Tiempo", value=str(e['Tiempo'][contador])+ ' min', delta=str(round(e['Tiempo'][contador]-e['Tiempo'].mean(),2)) + ' min', delta_color="inverse")
                st.metric(label="Agua", value=str(e['Agua'][contador])+ ' l', delta=str(round(e['Agua'][contador]-e['Agua'].mean(),2)) + ' l', delta_color="inverse")
                st.metric(label="Ruido", value=str(e['Ruido'][contador])+ ' dB', delta=str(round(e['Ruido'][contador]-e['Ruido'].mean(),2)) + ' dB', delta_color="inverse")
                st.metric(label="Puntuación", value=str(round(e['PA'][contador],1))+ ' p', delta=str(round(e['PA'][contador]-e['PA'].mean(),2)) + ' p')
                    
            st.write(str(e['Enlace'][contador]),unsafe_allow_html=True,)
    
    if contador + 1 < len(e):
        with col3:
            
            
            
                
                contador = 2
            
                st.subheader(str(contador+1) + ') ' + str(e['Marca'][contador]))
                st.text(str(e['Modelo'][contador]))
                
                st.image(e['Imagen'][contador], use_column_width=True)
                
                with st.expander("Ver características"):
                
                    st.metric(label="Capacidad", value=str(e['Capacidad'][contador]) + ' kg', delta=str(round(e['Capacidad'][contador]-e['Capacidad'].mean(),2)) + ' kg')
                    st.metric(label="Centrifugado", value=str(e['Centrifugado'][contador])+ ' RPM', delta=str(round(e['Centrifugado'][contador]-e['Centrifugado'].mean(),2)) + ' RPM')
                    st.metric(label="Energia", value=str(e['Energia'][contador])+ ' kwh', delta=str(round(e['Energia'][contador]-e['Energia'].mean(),2)) + ' kwh', delta_color="inverse")
                    st.metric(label="Tiempo", value=str(e['Tiempo'][contador])+ ' min', delta=str(round(e['Tiempo'][contador]-e['Tiempo'].mean(),2)) + ' min', delta_color="inverse")
                    st.metric(label="Agua", value=str(e['Agua'][contador])+ ' l', delta=str(round(e['Agua'][contador]-e['Agua'].mean(),2)) + ' l', delta_color="inverse")
                    st.metric(label="Ruido", value=str(e['Ruido'][contador])+ ' dB', delta=str(round(e['Ruido'][contador]-e['Ruido'].mean(),2)) + ' dB', delta_color="inverse")
                    st.metric(label="Puntuación", value=str(round(e['PA'][contador],1))+ ' p', delta=str(round(e['PA'][contador]-e['PA'].mean(),2)) + ' p')
                
                st.write(str(e['Enlace'][contador]),unsafe_allow_html=True,)
    



    
    


    with st.expander("Comparador y listado completo"):
        ver_por = st.selectbox(
        'Agrupar por:',
        ('Marcas', 'Lavadoras'))
        
        
        col1, col2 = st.columns(2)
        with col1:
            Comparar = st.selectbox(
            'Comparar:',
            (lista_comp), index=1)
        
        with col2:
            con = st.selectbox(
            'vs:',
            (lista_comp))
            
            
            
        option = pd.DataFrame()
        visu = []
        resultados = ""
      
        if ver_por == 'Marcas':
            option = grupo_marcas
            visu=['Marca']
            colo = 'Marca'
            resultados = 'Resultados: ' + str(len(grupo_marcas)) + ' marcas'
        else:
            option = e
            visu = ['Marca', 'Modelo']
            colo='Marca'
            resultados = 'Resultados: ' + str(len(e)) + ' lavadoras'
        
        
        c= alt.Chart(option).mark_circle(size=200).encode(
        alt.X(Comparar,
            scale=alt.Scale(zero=False, padding=1)
        ),
        alt.Y(con,
              scale=alt.Scale(zero=False, padding=1)
              
              ),
        tooltip = visu,   
        color = colo,
        
        ).configure_axis(grid=False).interactive(True)
        
        st.altair_chart(c, use_container_width=True)
        
        
        
        
    
    

        if ver_por == 'Marcas':
            st.table(grupo_marcas_punt.style.format({'CC': '{:.1f}', 'VC': '{:.1f}', 'CE': '{:.1f}', 'TL': '{:.1f}', 'CA': '{:.1f}', 'RL': '{:.1f}', 'PT': '{:.1f}', 'PA': '{:.1f}'}))
    
        else:  
            
            e = e[['Marca', 'Modelo', 'CC', 'VC', 'CE', 'TL', 'CA', 'RL', 'PA']]
            
            e.index = e['Modelo']
            
            e = e.drop('Modelo', axis=1)
            
            st.table(e.style.format({'CC': '{:.1f}', 'VC': '{:.1f}', 'CE': '{:.1f}', 'TL': '{:.1f}', 'CA': '{:.1f}', 'RL': '{:.1f}', 'PA': '{:.1f}'}))
        


    with st.expander("¿Cómo funciona?"):
        st.markdown(
            '''**¿Cómo funciona?**
            
Es muy sencillo, selecciona el tipo de carga (superior o frontal), el rango de capacidad en kg y las marcas en las que más confianza tengas.

**¿Cómo se determina si una lavadora es mejor que otra?**

A cada lavadora se le ha dado una puntuación, que resulta de haber medido las siguientes especificaciones:
- Capacidad
- Velocidad de centrifugado
- Consumo de energía
- Tiempo de lavado
- Consumo de agua
- Ruido




Lo explicamos mejor con un ejemplo. A una lavadora con una velocidad de centrifugado de 1.400 RPM se le otorgará una puntuación mayor que a una lavadora que su velocidad de centrifugado sea de 1.000 RPM.
Una vez obtenida la valoración de cada característica se hace una media entre ellas para conocer la puntuación que tendrá la lavadora en su conjunto.

En el apartado de Comparador y listado completo puedes ver la puntuación (PA) de cada lavadora y la puntuación de cada una de sus características.

**Ver características**

Puedes ver las especificaciones de cada lavadora desplegando el panel de características. También encontrarás una comparativa respecto a la media del resto de lavadoras. Un valor en verde indica que tiene una característica mejor que la media y un valor en rojo indica que es peor que la media de la selección actual.

**“La importancia” de cada una de las características**

De forma predeterminada, se ha asignado la misma importancia a todas las características. Pero nos podría interesar darle más importancia a alguna característica en concreto, por ejemplo:

Valoraremos mejor una lavadora con un consumo de energía bajo por lo que deberíamos puntuar con un valor cercano a 10. En cambio, podría no ser tan importante para nosotros el ruido de la lavadora mientras está centrifugando, por lo que le daríamos una puntuación más baja.

Una puntuación de 10 indica que le damos la máxima importancia, en cambio una puntuación de 0 no le dará ninguna importancia, por lo que a la hora de obtener la puntuación de la lavadora no tendrá en cuenta esta característica.
'''
                        
            )
