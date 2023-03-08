#!/usr/bin/env python
# coding: utf-8

# In[105]:


import pandas as pd


# In[106]:


from frappeclient import FrappeClient
from datetime import datetime
import os
from decouple import config


# In[107]:


import json


# In[108]:


client = FrappeClient("https://test-bullwork.frappe.cloud/")
client.authenticate(config('API_KEYD1'), config('API_SD1'))


# In[5]:


#client = FrappeClient("http://erpnext.localhost:8000/")
#client.authenticate(config('API_KEYL'), config('API_SL'))


# In[128]:


def get_item_template():
    doc = client.get_doc('Attributes of Category','Motor')
    attribute = pd.DataFrame.from_records(doc['define_attributes'])
    print(attribute)
    attribute =attribute[['attribute_name']]
    cat_name = pd.DataFrame({'attribute_name':['Motor']})
    attribute = pd.concat([cat_name, attribute]).reset_index(drop = True)
    attribute_t = attribute.set_index('attribute_name').T
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
        


# In[129]:


get_item_template()


# In[ ]:





# In[144]:


def gen_item_dms():
    item = pd.read_excel("D:/files/bullwork/sw_erpnext/" + "item_master_template" +
                              ".xlsx",skiprows=0,usecols = "B:H")

    item.fillna('')

    item.dropna(subset=['Motor'],inplace=True)


    item = item.fillna('')


    item['item_code']=''
    item['item_name']=''
    item['remarks']=''

    item_name = ''
    cdt = []
    crec = {}
    col = item.columns
    doc = {}
    for index,row in item.iterrows():
        for i in range(len(row)):
            if not row[i]=='':
                if i>0:
                    item_char =  client.get_value("Item character", ["numeric_values"], {"character_name": col[i] })
                    if item_char['numeric_values'] == 1:
                        item_name += col[i]+':'+str(row[i]) + ' '
                    else:
                        item_name += str(row[i]) + ' '
                    
                
                else:
                    item_name += str(row[i]) + ' '
        print(item_name)
        item_erp = client.get_value("Item dms", ["item_code","item_name"], {"item_name": item_name.rstrip() })
        print(item_erp)
        if item_erp:
            item.loc[index,'item_code']=item_erp['item_code']
            item.loc[index,'item_name']=item_erp['item_name']
            item.loc[index,'remarks']= 'This item already exist in ERP..' + item_erp['item_name'] + ' ' + item_erp['item_code']
            exit
        else:
            i=1
            for i in range(1,len(row)):
                if not row[i]=='':
                    print(col[i],row[i])
                
                    item_char =  client.get_value("Item character", ["numeric_values"], {"character_name": col[i] })
                    if item_char['numeric_values'] != 1:
                        crec['attribute_value']=row[i]
                               
                    crec['attribute'] = col[i]
                    crec['attribute_value_both']=row[i]
                    crec['attribute_of']=row[0]
                    cdt.append(crec)
                    crec = {}
                i += 1
            print(cdt)
            print(row)
            print(row[0])
            doc['maintain_attribute'] = 1
            doc['doctype'] = 'Item dms'
            doc['cat_name'] = row[0]
            doc['item_character'] = cdt
            doc['item_group'] = 'SP : Standard Part'
            doc['item_name'] = item_name.strip()
            doc['naming_series'] = doc['item_group'][:2]+'.#####'
            client.insert(doc)
        
            
                


# In[145]:


gen_item_dms()


# In[176]:


item_char =  client.get_doc("Item character",{'name': 'Size'})


# In[172]:


item_char


# In[191]:


doc = client.get_value('Item character',{'character_value': 'M4x10xP1.25'})


# In[192]:


doc


# In[ ]:




