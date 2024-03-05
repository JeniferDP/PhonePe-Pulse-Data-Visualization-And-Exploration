import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
import plotly.graph_objects as go
from PIL import Image
import base64
image=Image.open(r"C:\Users\Viswa.DP-PC\Desktop\images.png")

connection=psycopg2.connect(host="localhost",user="postgres",password="12345",database="phone_pe",port="5432")
mycursor=connection.cursor()

#agg_trans df
mycursor.execute("SELECT * from agg_trans")
connection.commit()
table1=mycursor.fetchall()

Aggregated_transaction= pd.DataFrame(table1,columns=("State","Year","Quarter","Transaction_type",
                                                        "Transaction_count","Transaction_amount"))

#agg_user df
mycursor.execute("SELECT * from agg_user")
connection.commit()
table2=mycursor.fetchall()

Aggregated_user= pd.DataFrame(table2,columns=("State","Year","Quarter","Brands",
                                                        "Count","Percentage"))   


#map-trans df         
mycursor.execute("SELECT * from map_trans")
connection.commit()
table3=mycursor.fetchall()

Map_transaction= pd.DataFrame(table3,columns=("State","Year","Quarter","District",
                                                        "Transaction_count","Transaction_amount"))  


#map-user df         
mycursor.execute("SELECT * from map_user")
connection.commit()
table4=mycursor.fetchall()

Map_user= pd.DataFrame(table4,columns=("State","Year","Quarter","District",
                                                        "Registered_users","App_opens"))  


#top-trans df         
mycursor.execute("SELECT * from top_trans")
connection.commit()
table5=mycursor.fetchall()

Top_transaction= pd.DataFrame(table5,columns=("State","Year","Quarter","Pincode",
                                                        "Transaction_count","Transaction_amount"))  


#top-user df         
mycursor.execute("SELECT * from top_user")
connection.commit()
table6=mycursor.fetchall()

Top_user= pd.DataFrame(table6,columns=("State","Year","Quarter","Pincode",
                                                        "Registered_user"))  
                                           
#Agg_transaction_amount function
def Transaction_amount_count_Y(df,year):
    tracy=df[df["Year"]==year]
    tracy.reset_index(drop=True,inplace=True)# to reset index

    tracy_group=tracy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tracy_group.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    
    with col1:
        fig_amount=px.bar(tracy,x="State",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_amount)
        


    with col2:
        fig_count=px.bar(tracy,x="State",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Burgyl_r,height=650,width=550)
        st.plotly_chart(fig_count)

        

    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)
        states=[]
        for feature in data["features"]:
            states.append(feature["properties"]["ST_NM"])

        states.sort()

        fig_India=px.choropleth(tracy_group, geojson=data, locations="State",featureidkey="properties.ST_NM", 
                                color="Transaction_amount",color_continuous_scale='tealrose',
                                range_color=(tracy_group["Transaction_amount"].min(),tracy_group["Transaction_amount"].max()),
                                hover_name="State", title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                 height=600,width=600)
        fig_India.update_geos(visible=False)
        st.plotly_chart(fig_India)


    with col2:

        fig_India1=px.choropleth(tracy_group, geojson=data, locations="State",featureidkey="properties.ST_NM", 
                            color="Transaction_count",color_continuous_scale='twilight',
                            range_color=(tracy_group["Transaction_count"].min(),tracy_group["Transaction_count"].max()),
                            hover_name="State", title=f"{year} TRANSACTION COUNT",fitbounds="locations", 
                            height=600,width=600)
        fig_India1.update_geos(visible=False)
        st.plotly_chart(fig_India1)

    return tracy

#Aggregated_quarter fn
def Transaction_amount_count_Q(df,quarter):
    tracq=df[df["Quarter"]==quarter]
    tracq.reset_index(drop=True,inplace=True)# to reset index

    tracq_group=tracq.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tracq_group.reset_index(inplace=True)
    
    col1,col2=st.columns(2)

    with col1:
        fig_amount=px.bar(tracq,x="State",y="Transaction_amount",
                        title=f" { tracq['Year'].min()}  YEAR {quarter} QUARTER  TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tracq,x="State",y="Transaction_count",
                        title=f" { tracq['Year'].min()}  YEAR {quarter} QUARTER  TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Burgyl_r)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)
        states=[]
        for feature in data["features"]:
            states.append(feature["properties"]["ST_NM"])

        states.sort()

        fig_India=px.choropleth (tracq_group, geojson=data, locations="State",featureidkey="properties.ST_NM", 
                                color="Transaction_amount",color_continuous_scale='tealrose',
                                range_color=(tracq_group["Transaction_amount"].min(),tracq_group["Transaction_amount"].max()),
                                hover_name="State", title=f"{ tracq['Year'].min()}  YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                                fitbounds="locations", height=800,width=800)
        fig_India.update_geos(visible=False)
        st.plotly_chart(fig_India)

    with col2:
        fig_India1=px.choropleth(tracq_group, geojson=data, locations="State",featureidkey="properties.ST_NM", 
                                color="Transaction_count",color_continuous_scale='twilight',
                                range_color=(tracq_group["Transaction_count"].min(),tracq_group["Transaction_count"].max()),
                                hover_name="State", title=f"{ tracq['Year'].min()}  YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations", height=800,width=800)
        fig_India1.update_geos(visible=False)
        st.plotly_chart(fig_India1)
    
    return tracq
     

def Transaction_type(df,state):

    tracy=df[df["State"] == state]
    tracy.reset_index(drop=True,inplace=True)

    tracy_group=tracy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tracy_group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_pie=px.pie(data_frame= tracy_group, names="Transaction_type", 
                        values="Transaction_amount",width=650,title= f"{state.upper()} TRANSACTION AMOUNT",
                        hole=0.5 ,)
        st.plotly_chart(fig_pie)

    with col2:
        fig_pie1=px.pie(data_frame= tracy_group, names="Transaction_type", 
                        values="Transaction_count",width=650,title= f"{state.upper()} TRANSACTION COUNT",
                        hole=0.5 )
        st.plotly_chart(fig_pie1)
    
       
#aggregated-user function
def agg_user(df,year):
    agguy=df[df["Year"]==year]
    agguy.reset_index(drop=True,inplace=True)


    agguy_g=pd.DataFrame(agguy.groupby("Brands")["Count"].sum())
    agguy_g.reset_index(inplace=True)


    fig_user=px.bar(agguy_g, x="Brands",y="Count",title=f"{year} BRANDS QUANTITY",width=850,
                    color_discrete_sequence=px.colors.sequential.Agsunset,hover_name="Brands")
    st.plotly_chart(fig_user)

    return agguy


#aggregated user analysis quarterly
def agg_user1(df,quarter):
    agguy_q=df[df["Quarter"]== quarter]
    agguy_q.reset_index(drop=True,inplace=True)

    agguyq_g=pd.DataFrame(agguy_q.groupby("Brands")["Count"].sum())
    agguyq_g.reset_index(inplace=True)

    fig_user1=px.bar(agguyq_g, x="Brands",y="Count",title=f"{quarter} QUARTER, BRANDS QUANTITY",width=850,
                        color_discrete_sequence=px.colors.sequential.Jet,hover_data="Brands")
    st.plotly_chart(fig_user1)
    
    return agguy_q


#aggregated user state analysis
def agg_user2(df,state):
    agguyqs=df[df["State"]== state]
    agguyqs.reset_index(drop=True,inplace=True)

    fig_user2=px.line(agguyqs,x="Brands",y="Count",hover_data="Percentage",
                    title=f"{state.upper()} PERCENTAGE OF BRANDS QUANTITY",width=1000,markers=True,
                    color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_user2)



#map_trans_district analysis
def Map_Trans_dist(df,state):

    tracy=df[df["State"]==state]
    tracy.reset_index(drop=True,inplace=True)

    tracy_group=tracy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tracy_group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_map=px.bar(tracy_group, x="Transaction_amount",y="District",orientation="h",height=600,width=600,
                        title=f"{state.upper()} DISTRICT TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.OrRd_r)
        st.plotly_chart(fig_map)

    with col2:

        fig_map1=px.bar(tracy_group, x="Transaction_count",y="District",orientation="h",height=600,width=600,
                        title=f"{state.upper()} DISTRICT TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Purp_r)
        st.plotly_chart(fig_map1)

    
#map-user function
def map_user(df,year):
    muy=df[df["Year"]== year]
    muy.reset_index(drop=True,inplace=True)


    muy_g=pd.DataFrame(muy.groupby("State")[["Registered_users","App_opens"]].sum())
    muy_g.reset_index(inplace=True)



    fig_mapuser=px.line(muy_g, x="State",y=["Registered_users","App_opens"],
                        title=f"{year} APP USERS",color_discrete_sequence=px.colors.sequential.Blackbody ,
                        width=850,height=850,        
                        markers=True)
    st.plotly_chart(fig_mapuser)



    return muy  

#map-user1 function
def map_user1(df,quarter):
    muyq=df[df["Quarter"]== quarter]
    muyq.reset_index(drop=True,inplace=True)


    muyq_g=pd.DataFrame(muyq.groupby("State")[["Registered_users","App_opens"]].sum())
    muyq_g.reset_index(inplace=True)



    fig_mapuser1=px.line(muyq_g, x="State",y=["Registered_users","App_opens"],
                        color_discrete_sequence=px.colors.sequential.Magenta_r,
                        title=f"{df['Year'].min()} YEAR {quarter} QUARTER APP USERS",width=1000,height=900,       
                        markers=True)
    st.plotly_chart(fig_mapuser1)



    return muyq     

#map-user2 function
def map_user2(df,state):
    muyqs=df[df["State"]== state]
    muyqs.reset_index(drop=True,inplace=True)


    fig_mapuser2=px.bar(muyqs, x="Registered_users",y="District",orientation="h",
                        color_discrete_sequence=px.colors.sequential.amp_r,
                        title=f"{state} REGISTERED USERS",height=600    
                        )
    st.plotly_chart(fig_mapuser2)


#top_transaction
def top_trans_y(df,state):
    toty= df[df["State"]==state]
    toty.reset_index(drop=True,inplace=True)

    toty_group=toty.groupby("Pincode")[["Transaction_count","Transaction_amount"]].sum()
    toty_group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_top=px.bar(toty, x="Quarter",y="Transaction_amount", hover_data="Pincode",
                        title=f"{state.upper()} TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Bluered)
        st.plotly_chart(fig_top)
    with col2:
        fig_top1=px.bar(toty, x="Quarter",y="Transaction_count",hover_data="Pincode",
                        title= f"{state.upper()} TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_top1)


#top-user function
def top_user(df,year):
    tuy=df[df["Year"]== year]
    tuy.reset_index(drop=True,inplace=True)


    tuy_g=pd.DataFrame(tuy.groupby(["State", "Quarter"])["Registered_user"].sum())
    tuy_g.reset_index(inplace=True)

    fig_topuser=px.bar(tuy_g, x="State",y="Registered_user", color="Quarter",
                            color_discrete_sequence=px.colors.sequential.algae_r,
                            title=" TOP USERS",width=850,height=850,hover_name="State"      
                            )
    st.plotly_chart(fig_topuser)

    return tuy


#top-user2 function
def top_user1(df,state):
    tuys=df[df["State"]== state]
    tuys.reset_index(drop=True,inplace=True)


    fig_topuser1=px.bar(tuys, x="Quarter",y="Registered_user",
                                color_continuous_scale =px.colors.sequential.Magenta_r,
                                title=f"{state.upper()} TOP USERS",width=850,height=850,
                                hover_data="Pincode",color="Registered_user" ,hover_name="State"    
                                )

    st.plotly_chart(fig_topuser1)


#top app users
def ques1():
    app=Map_user[["App_opens","State","Year"]]
    app.reset_index(drop=True,inplace=True)

    app_g=app.groupby(["State","Year"])["App_opens"].sum().sort_values(ascending=False)
    apps=pd.DataFrame(app_g).reset_index().head(20)

    fig_app=px.bar(apps,x="State",y="App_opens",color="Year",title="TOP APP USERS(YEARLY",
                    color_discrete_sequence=px.colors.sequential.swatches_continuous,hover_name="State")
    return st.plotly_chart(fig_app)
    

#top 10 states with high TA

def ques2():
    state=Aggregated_transaction[["State","Transaction_amount"]]
    state.reset_index(drop=True,inplace=True)

    state_g=state.groupby("State")["Transaction_amount"].sum().sort_values(ascending=False)
    states=pd.DataFrame(state_g).reset_index().head(10)

    fig_state=px.line(states,x="State",y="Transaction_amount",title="TOP 10 STATES WITH HIGHEST TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.BuGn_r,
                                hover_name="State",markers=True)
    return st.plotly_chart(fig_state)



#top 10 dist with high TA
def ques3():
        district=Map_transaction[["District","State","Transaction_amount"]]
        district.reset_index(drop=True,inplace=True)

        dis_g=district.groupby(["District","State"])["Transaction_amount"].sum().sort_values(ascending=False)
        districts=pd.DataFrame(dis_g).reset_index().head(10)

        fig_district=px.bar(districts,x=["District","State"],y="Transaction_amount",title="TOP 10 DISTRICT WITH HIGHEST TRANSACTION AMOUNT",
                                color_discrete_sequence=px.colors.sequential.BuPu_r,
                                        hover_name="District")
        return st.plotly_chart(fig_district)
  
#top 15 states with high TC
def ques4():
    state1=Aggregated_transaction[["State","Transaction_count"]]
    state1.reset_index(drop=True,inplace=True)

    sta_g=state1.groupby("State")["Transaction_count"].sum().sort_values(ascending=False)
    stat=pd.DataFrame(sta_g).reset_index().head(15)

    fig_qua=px.pie(data_frame=stat,values="Transaction_count", names="State",
                    color_discrete_sequence=px.colors.sequential.dense, 
                    title="TOP 15 STATES HIGHEST TRANSACTION COUNT",hover_name="State")
    return st.plotly_chart(fig_qua)

#top registered users(quartlerly)
def ques5():
    dist=Map_user[["State","Quarter","Registered_users"]]
    dist.reset_index(drop=True,inplace=True)


    dist_g=dist.groupby(["Quarter","State"])["Registered_users"].sum().sort_values(ascending=False)
    districts=pd.DataFrame(dist_g).reset_index().head(10)

    fig_reg=px.bar(districts,x=["State","Quarter"],y="Registered_users",title="TOP REGISTERED USERS(QUARTERLY)",
                    color_discrete_sequence=px.colors.sequential.Bluyl_r,hover_name="State")
    return st.plotly_chart(fig_reg)

#lowest transaction amount-district
def ques6():
    district=Map_transaction[["District","State","Transaction_amount"]]
    district.reset_index(drop=True,inplace=True)

    dis_g=district.groupby(["District","State"])["Transaction_amount"].sum().sort_values(ascending=True)
    districts=pd.DataFrame(dis_g).reset_index().head(10)

    fig_district=px.bar(districts,x=["District","State"],y="Transaction_amount",title="TOP 10 DISTRICT WITH LOWEST TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Cividis,
                                    hover_name="District")
    return st.plotly_chart(fig_district)

#states with low TA
def ques7():
    state2=Aggregated_transaction[["State","Transaction_amount"]]
    state2.reset_index(drop=True,inplace=True)

    state_g=state2.groupby("State")["Transaction_amount"].sum().sort_values(ascending=True)
    states=pd.DataFrame(state_g).reset_index().head(10)

    fig_state1=px.line(states,x="State",y="Transaction_amount",title="TOP 10 STATES WITH LOWEST TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.PuBuGn_r,
                                hover_name="State",markers=True)
    return st.plotly_chart(fig_state1)

#lowest state TC
def ques8():
    state1=Top_transaction[["State","Transaction_count"]]
    state1.reset_index(drop=True,inplace=True)

    sta_g=state1.groupby("State")["Transaction_count"].sum().sort_values(ascending=True)
    stat=pd.DataFrame(sta_g).reset_index().head(15)

    fig_qua1=px.pie(data_frame=stat,values="Transaction_count", names="State",
                    color_discrete_sequence=px.colors.sequential.dense, 
                    title="TOP 15 STATES LOWEST TRANSACTION COUNT",hover_name="State")
    return st.plotly_chart(fig_qua1)

#lowest district TC
def ques9():
    district1=Map_transaction[["District","State","Transaction_count"]]
    district1.reset_index(drop=True,inplace=True)

    dis_g=district1.groupby(["District","State"])["Transaction_count"].sum().sort_values(ascending=True)
    districts=pd.DataFrame(dis_g).reset_index().head(30)

    fig_district1=px.bar(districts,x=["District","State"],y="Transaction_count",title="TOP DISTRICTS WITH LOWEST TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Magenta_r,
                                    hover_name="District")
    return st.plotly_chart(fig_district1)

#highest districts TC
def ques10():
        district2=Map_transaction[["District","State","Transaction_count"]]
        district2.reset_index(drop=True,inplace=True)

        dis_g=district2.groupby(["District","State"])["Transaction_count"].sum().sort_values(ascending=False)
        districts=pd.DataFrame(dis_g).reset_index().head(30)

        fig_district2=px.bar(districts,x=["District","State"],y="Transaction_count",title="TOP DISTRICTS WITH HIGHEST TRANSACTION COUNT",
                                color_discrete_sequence=px.colors.sequential.Rainbow_r,
                                        hover_name="District")
        return st.plotly_chart(fig_district2)



    
    

#streamlit
st.set_page_config(layout="wide")
st.title("PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    st.image(image,caption="PhonePe Pulse" )
    select=option_menu("Main menu",["Home","Explore Data","Top Facts"])

if select=="Home":
    st.write("")
    st.write("")
    st.write("")
    st.subheader("****PHONEPE- INDIA'S BEST TRANSACTION APP****")
    col1,col2= st.columns(2)
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        image=Image.open(r"C:\Users\Viswa.DP-PC\Desktop\phonepe\1581678740.jpg")
        st.image(image)
    
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.video(r"C:\Users\Viswa.DP-PC\Desktop\phonepe\Phone Pe Ad.mp4")

    
    
    st.video(r"C:\Users\Viswa.DP-PC\Desktop\phonepe\Purple Sky Profile Header.mp4")   

    col6,col7=st.columns(2)
    
    with col6:
        st.write("")
        st.write("")
        st.write("")
        mygif = base64.b64encode(open(r"C:\Users\Viswa.DP-PC\Desktop\phonepe\image_processing20200114-26356-1dzvejl.gif", 'rb').read()).decode()
        st.markdown(f"""<img src="data:png;base64,{mygif}" width='600' height='370' >""", True)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
    with col7:
        st.write("")
        st.write("")
        st.write("")
        st.video(r"C:\Users\Viswa.DP-PC\Desktop\phonepe\You can quickly pay with no PIN with UPI lite on PhonePe.mp4")
        st.link_button(":red[DOWNLOAD THE APP NOW]", "https://www.phonepe.com/app-download/")

elif select=="Explore Data":
    tab1,tab2,tab3=st.tabs(["Aggregated ","Map","Top"])

    with tab1:
        method=st.selectbox("Analysis type",["--Please select the value--","Aggregated Transaction","Aggregated User"])

        if method=="Aggregated Transaction":
            col1,col2=st.columns(2)
            st.subheader("Yearly Analysis")
            with col1:
                years=st.slider("Select the year",Aggregated_transaction["Year"].min(),Aggregated_transaction["Year"].max(),Aggregated_transaction["Year"].min())
            tracy_1= Transaction_amount_count_Y(Aggregated_transaction, years) 

            col1,col2=st.columns(2)
            st.subheader("Quarterly Analysis")
            with col1:
                quarters=st.selectbox("Select the quarter",tracy_1["Quarter"].unique())
            tracy_q=Transaction_amount_count_Q(tracy_1,quarters)

            col1,col2=st.columns(2)
            st.subheader("State-Wise Payment Types (Quarterly)")
            with col1:
                states=st.selectbox("Select The State", tracy_q["State"].unique())

            Transaction_type(tracy_q,states)

            col1,col2=st.columns(2)
            st.subheader("State-Wise Payment Types (Yearly)")
            with col1:
                states=st.selectbox("Select The States", tracy_1["State"].unique())

            Transaction_type(tracy_1,states)


        elif method=="Aggregated User":

            col1,col2=st.columns(2)
            st.subheader("Users Brand Yearly Analysis")
            with col1:
                years=st.slider("Select the year",Aggregated_user["Year"].min(),Aggregated_user["Year"].max(),Aggregated_user["Year"].min())
            agg_user_year=agg_user(Aggregated_user,years)


            col1,col2=st.columns(2)
            st.subheader("Users Brand Quarterly Analysis")
            with col1:
                quarters=st.slider("Select the quarter_a",agg_user_year["Quarter"].min(),agg_user_year["Quarter"].max(),agg_user_year["Quarter"].min())
            agg_user_year_q=agg_user1(agg_user_year,quarters)

            col1,col2=st.columns(2)
            st.subheader("State Users Analysis")
            with col1:
                states=st.selectbox("Select The State_a", agg_user_year_q["State"].unique())

            agg_user2(agg_user_year_q,states)

    with tab2:
        method1=st.selectbox("Analysis type",["--Please select the value--","Map Transaction","Map User"])

        if method1=="Map Transaction":
            st.subheader("Yearly Analysis")
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select The Year",Map_transaction["Year"].min(),Map_transaction["Year"].max(),Map_transaction["Year"].min())
            
            map_trac_y=Transaction_amount_count_Y(Map_transaction,years)

            col1,col2=st.columns(2)
            st.subheader("State-wise Transaction Analysis")
            with col1:
                states=st.selectbox("Select The States", map_trac_y["State"].unique())

            Map_Trans_dist(map_trac_y,states)

            col1,col2=st.columns(2)
            st.subheader("Quarterly Analysis")
            with col1:
                quarters=st.selectbox("Select the quarter",map_trac_y["Quarter"].unique())
            map_tr_y_q=Transaction_amount_count_Q(map_trac_y,quarters)

            col1,col2=st.columns(2)
            st.subheader("District Transaction Analysis")
            with col1:
                states=st.selectbox("Select The State-M", map_tr_y_q["State"].unique())

            Map_Trans_dist(map_tr_y_q,states)

        elif method1=="Map User":
            st.subheader("Registered App Users")
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select the year",Map_user["Year"].min(),Map_user["Year"].max(),Map_user["Year"].min())
            map_user_y=map_user(Map_user,years)

            col1,col2=st.columns(2)
            st.subheader("Registered App Users(Quarterly)")
            with col1:
                quarters=st.selectbox("Select the quarter",map_user_y["Quarter"].unique())
            map_user_y_q=map_user1(map_user_y,quarters)


            col1,col2=st.columns(2)
            st.subheader("District-wise Registered App Users")
            with col1:
                states=st.selectbox("Select The State", map_user_y_q["State"].unique())

            map_user2(map_user_y_q,states)




    with tab3:
        method3=st.selectbox("Analysis type",["--Please select the value--","Top Transaction","Top User"])

        if method3=="Top Transaction":
            st.subheader("Yearly Analysis")
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select The Year-T",Top_transaction["Year"].min(),Top_transaction["Year"].max(),Top_transaction["Year"].min())
            
            top_tr_y=Transaction_amount_count_Y(Top_transaction,years)

            col1,col2=st.columns(2)
            st.subheader("State-wise Transaction Analysis")
            with col1:
                states=st.selectbox("Select The State_t", top_tr_y["State"].unique())

            top_trans_y(top_tr_y,states)

            col1,col2=st.columns(2)
            st.subheader("Quarterly Analysis")
            with col1:
                quarters=st.selectbox("Select the quarter-t",top_tr_y["Quarter"].unique())
            top_tr_y_q=Transaction_amount_count_Q(top_tr_y,quarters)

        elif method3=="Top User":
            col1,col2=st.columns(2)
            st.subheader("Registered Users(Quarterly)")
            with col1:
                years=st.slider("Select The Year-TU",Top_user["Year"].min(),Top_user["Year"].max(),Top_user["Year"].min())
            
            top_user_y=top_user(Top_user,years)


            col1,col2=st.columns(2)
            st.subheader("District-wise Registered Users")
            with col1:
                states=st.selectbox("Select The State-TU", top_user_y["State"].unique())

            top_user1(top_user_y,states)


elif select=="Top Facts":
    
    ques= st.selectbox("**FACTS**",('Select Any One',
                                                'Top App users Yearly',
                                                'States With Highest Transaction Amount',
                                                'States With Lowest Transaction Amount',
                                                'Districts With Highest Transaction Amount',
                                                'Districts With Lowest Transaction Amount',
                                                'States With Highest Transaction Count',
                                                'States With Lowest Transaction Count',
                                                'Top registered users(quarterly)',
                                                'Districts With Lowest Transaction Count',
                                                'Districts With Highest Transaction Count'
                                                ))
                                    

    if ques=='Top App users Yearly':
        ques1()
    
    if ques=='States With Highest Transaction Amount':
        ques2()

    if ques=='States With Lowest Transaction Amount':
        ques7()
    
    if ques=='Districts With Highest Transaction Amount':
        ques3()

    if ques=='Districts With Lowest Transaction Amount':
        ques6()

    if ques == 'States With Highest Transaction Count':
        ques4()

    if ques == 'States With Lowest Transaction Count':
        ques8()
        
    if ques=='Top registered users(quarterly)':
        ques5()  

    if ques=='Districts With Lowest Transaction Count':
        ques9()

    if ques=='Districts With Highest Transaction Count':
        ques10()
    
    