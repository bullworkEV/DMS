#!/usr/bin/env python
# coding: utf-8

# In[105]:


import pandas as pd


# In[193]:


from frappeclient import FrappeClient
from datetime import datetime
import os
from decouple import config


# In[194]:


import json


# In[195]:


client = FrappeClient("https://test-bullwork.frappe.cloud/")
client.authenticate(config('API_KEYD1'), config('API_SD1'))


# In[196]:


#client = FrappeClient("http://erpnext.localhost:8000/")
#client.authenticate(config('API_KEYL'), config('API_SL'))


# In[334]:


def get_item_template():
    print("Category?")
    categ = input()
    doc = client.get_doc('Attributes of Category',categ)
    attribute = pd.DataFrame.from_records(doc['define_attributes'])
    print(attribute)
    attribute =attribute[['attribute_name']]
    cat_name = pd.DataFrame({'attribute_name':[categ]})
    attribute = pd.concat([cat_name, attribute]).reset_index(drop = True)
    attribute_t = attribute.set_index('attribute_name').T
    attribute_t['stock_uom']='Nos'
    attribute_t['Part Number']=''
    attribute_t['Drawing version']=''
    excel_file=pd.ExcelWriter("D:/files/bullwork/sw_erpnext/" + "item_master_template" +
                              '.xlsx')
    attribute_t.to_excel(excel_file,
             sheet_name='Template')
    attribute_t.to_excel(excel_file,
             sheet_name='Template',startcol=10)
    startcol=11
    for index,row in attribute.iterrows():
        if index > 0:
            doc1 = client.get_doc('Item character',row.attribute_name)
            char = pd.DataFrame.from_records(doc1['item_character_values'])
            if len(char)>0:
                char = char[['character_value']]
                char.to_excel(excel_file,
                     sheet_name='Template',startcol=startcol,startrow=2,index=False)
        startcol += 1
    excel_file.save()
    excel_file.close()
    print("Template downloaded ")
        


# In[335]:


get_item_template()


# In[ ]:





# In[370]:


def gen_item_dms():
    item_drg = []
    item = pd.read_excel("D:/files/bullwork/sw_erpnext/" + "item_master_template" +
                              ".xlsx",skiprows=0,usecols = "B:K")

    item.fillna('')

    item.dropna(subset=[item.loc[0][0]],inplace=True)


    item = item.fillna('')
    item['Drawing version']=item['Drawing version'].astype(str)


    item['item_code']=''
    item['item_name']=''
    item['remarks']=''

    item_name = ''
    cdt = []
    crec = {}
    col = item.columns
    doc = {}
    for index,row in item.iterrows():
        print(len(row))
        for i in range(len(row)):
            print(col[i],row[i])
            if not row[i]=='':
                if i>0:
                    print(col[i])
                    item_char =  client.get_value("Item character", ["numeric_values"], {"character_name": col[i] })
                    if len(item_char)>0 and item_char['numeric_values'] == 1:
                        item_name += col[i]+':'+str(row[i]) + ' '
                    else:
                        item_name += str(row[i]) + ' '
                    
                
                else:
                    item_name += str(row[i]) + ' '
        print(item_name)
        item_erp = client.get_value("Item dms", ["item_code","item_name"], {"item_name": item_name.rstrip() })
        if row['Part Number']:
            item_drg = client.get_value("Item dms", ["item_code","manual_part_number"], {"manual_part_number": row['Part Number'] })
        #print(item_erp)
        #print(item_drg)
        if item_erp:
            item.loc[index,'item_code']=item_erp['item_code']
            item.loc[index,'item_name']=item_erp['item_name']
            item.loc[index,'remarks']= 'This item already exist in ERP..' + item_erp['item_name'] + ' ' + item_erp['item_code']
            exit
        elif len(item_drg)>0:
            item.loc[index,'item_code']=item_drg['item_code']
            item.loc[index,'item_name']=item_drg['manual_part_number']
            item.loc[index,'remarks']= 'This drawing already exist in ERP..' + item_drg['manual_part_number'] + ' ' + item_drg['item_code']
            exit
        else:
            i=1
            for i in range(1,len(row)):
                if not row[i]=='':
                    print(col[i],row[i])
                
                    item_char =  client.get_value("Item character", ["numeric_values"], {"character_name": col[i] })
                    print(item_char)
                    if len(item_char)>0:
                        if item_char['numeric_values'] != 1:
                            crec['attribute_value']=str(row[i])
                               
                        crec['attribute'] = col[i]
                        crec['attribute_value_both']=str(row[i])
                        crec['attribute_of']=row[0]
                        cdt.append(crec)
                        crec = {}
                i += 1
            print(cdt)
            print(row)
            print(row[0])
            doc['stock_uom']=row['stock_uom']
            doc['manual_part_number']=row['Part Number']
            doc['version']=row['Drawing version']
            doc['description']=item_name.strip()
            doc['maintain_attribute'] = 1
            doc['doctype'] = 'Item dms'
            doc['cat_name'] = row[0]
            doc['item_character'] = cdt
            doc['item_group'] = 'SP : Standard Part'
            doc['item_name'] = item_name.strip()
            doc['naming_series'] = doc['item_group'][:2]+'.#####'
            client.insert(doc)
            cdt=[]
            crec={}
        item_name = ''
    excel_file=pd.ExcelWriter("D:/files/bullwork/sw_erpnext/" + "item_master_output" +
                              '.xlsx')
    item.to_excel(excel_file,
             sheet_name='Output')
    excel_file.save()
    excel_file.close()
    return item
        
            
                


# In[ ]:


if __name__=="__main__":
    get_item_template()
    gen_item_dms()


# In[372]:


item = gen_item_dms()
