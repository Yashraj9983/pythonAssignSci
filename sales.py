#first search then sort, instead of first sort then search
import pandas as pd  

def findPL(pls,query):
    for i in query.split(" "):        
        for pl in pls:
            if i in pl.lower():
                return pl
    return ""        

def findBrand(brands,query):    
    for brand in brands:
        if brand.lower() in query:
            return brand
    return ""
              

def leastCheck(query,df):
    indexToDrop=[]
    for i in df.index :
        valid=1
        for word in query.split(" "):
            prod_name=df["sku"][i]+" "+df["product_line"][i]+" "+df["brand"][i]
            prod_name=prod_name.lower()
            if word not in prod_name:
                valid-=1
        # print(i,valid)
        if len(query.split(" "))>1:
            if valid<0:
                indexToDrop.append(i)
        else:
            if valid<1:
                indexToDrop.append(i)
    
    df.drop(indexToDrop , inplace=True)
    return df              

def searchEngine(query,df,brands,product_lines):
    df2=df.copy()

    brand=findBrand(brands,query)
    if brand!="":
        df2=df2.loc[df2["brand"]==brand]
    # print(df2)    

    pl=findPL(product_lines,query)
    # print(pl)
    if pl!="":
        df2=df2.loc[df2["product_line"]==pl]
    # print(df2)    

    df2=leastCheck(query,df2)
    # print("final")
    # print(df2)    
                    
    # print("\nTop Selling Products :\n",df2.nlargest(3,["sales"]).to_string(index=False))
    # print("\nLowest Price Products :\n",df2.nsmallest(3,["price"]).to_string(index=False))
    # print("\nHighest Price Products :\n",df2.nlargest(3,["price"]).to_string(index=False))    

    print("\nTop Selling Products :\n",df2.nlargest(3,["sales"])[["SKU_ID","sku"]].to_string(index=False))
    print("\nLowest Price Products :\n",df2.nsmallest(3,["price"])[["SKU_ID","sku"]].to_string(index=False))
    print("\nHighest Price Products :\n",df2.nlargest(3,["price"])[["SKU_ID","sku"]].to_string(index=False)) 

def main():
    df = pd.read_csv("sales_data.csv")  
    df=df.replace({r'\r': ''}, regex=True)
    brands=df["brand"].unique()
    product_lines=df["product_line"].unique()
    while(True):
        print("\nEnter search text:")
        query=input()    
        query=query.lower()
        searchEngine(query,df,brands,product_lines)

if __name__=="__main__":
    main()
