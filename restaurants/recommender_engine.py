import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pickle
import sys
import gc
from scipy import sparse
from scipy.sparse import csr_matrix
from lightfm.data import Dataset
import lightfm
import os



class Recommendation():

    def __init__(self, user_input_dct, location):
        self.user_input_dct = user_input_dct
        self.model = Recommendation._load_saved_dataset('model_93')
        self.user_feature_map = Recommendation._load_saved_dataset('user_feature_map')
        self.user_feature_columns = Recommendation._load_saved_dataset('user_feature_columns')
        self.rests_info_df = Recommendation._load_saved_dataset('rests_info_df')
        self.raw_item_map = Recommendation._load_saved_dataset('item_mapping')
        self.item_mapping = {y:x for x,y in self.raw_item_map.items()}
        self.rests_city_list = Recommendation._load_saved_dataset('rests_city_list')
        self.location = location
        self.n_items = len(self.item_mapping)
        self.FILTER_LIMIT = 100000000 # Limits number of recommended indexes of rests for mapping. 

    def give_recommendation(self):
        input_features_lst = ['cuisines', 'spec_diet', 'meals','features']
        for feature in input_features_lst:
            if feature not in self.user_input_dct:
                self.user_input_dct[feature] = []
        print(self.user_input_dct)
        self.new_user_features = self.preprocess_user_input(self.user_input_dct, self.user_feature_columns)
        result = self.predict(self.model, self.n_items, self.new_user_features, self.item_mapping,self.rests_info_df, self.rests_city_list, self.location)
        return result


    def preprocess_user_input(self, user_input_dct, user_feature_columns):
        '''
        Input: 
            Dictionary
        Output:
            sparse matrix of type '<class 'numpy.float64'>'
        
        '''
        # user_features_columns
        user_input_features = ['meals', 'features', 'cuisines', 'spec_diet', 'rest_types','price_tag_names','michelin_label',
                        'trav_choice_label', 'order_online', 'safety_measures']
        
        user_input_df = pd.DataFrame(columns=user_input_features)

        for key, value in user_input_dct.items():
            #user_input_df[key] = value
            if isinstance(value,list):
                user_input_df[key] = user_input_df[key].astype('object')
                user_input_df.at[1, key] = value
            else:
                user_input_df[key] = value
                
        # Dataframe contains only filled columns
        user_input_prep_df = Recommendation._create_user_input_features(user_input_df)
        
        # Dataframe 
        empty_user_features_df = pd.DataFrame(columns=user_feature_columns)
        empty_user_features_df.loc[1] = 0
        
        for col in user_input_prep_df.columns:
            try:
                empty_user_features_df[col] = 1
            except KeyError:
                print("Column not found while filling user features dataframe")
        
        user_input_features_lst = Recommendation._format_user_input_features(empty_user_features_df,user_feature_columns)
        
        new_user_features = Recommendation._format_newuser_input(self.user_feature_map, user_input_features_lst)
        
        return new_user_features
        #model, n_items, new_user_features, item_id_map, rests_info_df, rests_city_list
    def predict(self, model, n_items, new_user_features, item_mapping, rests_info_df, rests_city_list, location):
            
        scores = model.predict(0, np.arange(n_items), user_features = new_user_features)
        
        if self.FILTER_LIMIT > len(scores):
            self.FILTER_LIMIT == len(scores)

        items_index_lst = scores.argsort()[::-1][:self.FILTER_LIMIT]

        item_id_lst = [item_mapping[value] for value in items_index_lst]
        
        rests_info_df = rests_info_df[rests_info_df['rest_id'].isin(item_id_lst)]

        if location in rests_city_list:
            rests_info_df = rests_info_df[rests_info_df['rest_city'] == location]
        else:
            print('Input location not found')

        res_dict_lst = rests_info_df.to_dict('records')
        return res_dict_lst
    
    @classmethod
    # Importing and exporting functions
    def _load_saved_dataset(cls, filename):
        try:
            with open('restaurants/data/{}.pickle'.format(filename), 'rb') as fin:
                X = pickle.load(fin)
            print('Dataset loaded')
        except FileNotFoundError:
            print('File with saved dataset not found')
        return X

    @classmethod
    def _export_df(cls, X, filename='X'):
        try:
            with open('restaurants/data/{}.pickle'.format(filename), 'wb') as fout:
                pickle.dump(X, fout)
            print('Preprocessed dataframe exported')
        except FileNotFoundError:
            print('File not found')

    # Supplementary functions
    # Dealing with awards list of lists
    @classmethod
    def _unpack_list(cls, var):
        fin_str = ''
        for lst in var:
            if isinstance(var, list):
                s = lst[1]
                fin_str += s
                fin_str += ','
        return fin_str

    # Awards list
    @classmethod    
    def _awards_to_str(cls, merged,col):
        merged[col] = merged[col].apply(lambda x: Recommendation._unpack_list(x) if isinstance(x, list) else x)

        
    # Dealing with lists of values in columns    
    @classmethod
    def _convert_to_str(cls, merged,col):
        merged[col] = merged[col].apply(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)
        
    # Takes "merged" df and returns new df after preprocessing and joining merged to dummies
    @classmethod
    def _get_dummies(cls, df, col):

        dummy_df = df[col].str.get_dummies(sep=',')
        dummies_col_lst = dummy_df.columns
        dummies_col_set = set(dummies_col_lst)
        
        # If '0' is in column names, rename the column
        if '0' in dummy_df.columns:
            dummy_df.rename(columns={'0':str('no_info_' + col)}, inplace=True)
        
        df = df.drop(col,axis = 1)
        df = df.join(dummy_df)
        
        # Check for duplicate columns
        if len(dummies_col_lst) == len(dummies_col_set):
            print(f"{col} - No duplicates")
            print(f"                    - {len(dummies_col_lst)} columns created")
        else:
            print(f"{col} - Duplicates found")
            
        return df

    @classmethod
    def _create_user_input_features(cls, merged):

        nan_cols = list(merged[merged.columns[merged.isna().any()]].columns)
        
        # Replacing all NANs with 0s
        for col in nan_cols:
            merged[col] = merged[col].fillna(0)
            
        cols_with_lists = ['cuisines', 'spec_diet', 'meals', 'features','price_tag_names','rest_types','spec_diet']

        for col in cols_with_lists:
            Recommendation._convert_to_str(merged, col)
            
        
        # Sorting columns

        # Columns for dummy encoding
        cols_dummy = ['cuisines', 'spec_diet', 'meals','features']
        cols_dummy_no_sep = ['michelin_label','trav_choice_label']

        # Columns for binary labels encoding
        cols_binary_labels = ['order_online','safety_measures']

        # Text features  rest_id - excluded
        col_text = ['tag_cloud','about']
        #print(merged[cols_dummy].head())
        
        for col in cols_dummy:
            #print("Dummying: ", col)
            #print('Merged value; ', merged[col])
            merged = Recommendation._get_dummies(merged, col)
            
        # Dummies without separators
        merged = pd.get_dummies(merged, columns=['michelin_label'], prefix=["michelin_lbl_"])
        merged = pd.get_dummies(merged, columns=['trav_choice_label'], prefix=["travchoice_lbl_"])
        
        for col in cols_binary_labels:
            merged[col] = np.where(merged[col] == 0, 0, 1)

        
        merged.rename(columns={'michelin_lbl__0':'michelin_no_lbl'}, inplace=True)
        merged.rename(columns={"michelin_lbl__Travelers' Choice":'michelin_lbl'}, inplace=True)
        merged.rename(columns={"michelin_lbl__Travelers' Choice Best of the Best":'michelin_best_lbl'}, inplace=True)
        merged.rename(columns={'travchoice_lbl__0':'travchoice_no_lbl'}, inplace=True)
        merged.rename(columns={"travchoice_lbl__Travelers' Choice":'travchoice_lbl'}, inplace=True)
        merged.rename(columns={"travchoice_lbl__Travelers' Choice Best of the Best":'travchoice_best_lbl'}, inplace=True)

        return merged

    @classmethod
    def _format_user_input_features(cls, data, feature_columns):
        for i, row in data.iterrows():
            feature_values_lst = []
            for col_name in feature_columns:
                col_value = row[col_name]
                val = str(col_name) +":"+ str(col_value)
                feature_values_lst.append(val)
            return feature_values_lst

    @classmethod
    def _format_newuser_input(cls, user_feature_map, user_feature_list):
        num_features = len(user_feature_list)
        normalised_val = 1.0 
        target_indices = []
        for feature in user_feature_list:
            try:
                target_indices.append(user_feature_map[feature])
            except KeyError:
                print("new user feature encountered '{}'".format(feature))
                pass

        new_user_features = np.zeros(len(user_feature_map.keys()))
        for i in target_indices:
            new_user_features[i] = normalised_val
        new_user_features = sparse.csr_matrix(new_user_features)
        return (new_user_features)



def main():           
  # exercise the class methods

    user_input_dct = {}

    user_input_dct['meals'] = ['Dinner','Lunch']
    user_input_dct['features'] = ['Accepts Credit Cards','Accepts Visa','Free Wifi','Gift Cards Available']
    user_input_dct['cuisines'] = ['American','German','Greek','European']
    user_input_dct['spec_diet'] = ['Vegetarian Friendly']
    user_input_dct['rest_types'] = ['Restaurants']
    user_input_dct['price_tag_names'] = ['Fine Dining','Mid-range']
    user_input_dct['michelin_label'] = 0
    user_input_dct['trav_choice_label'] = 1
    user_input_dct['order_online'] = 1
    user_input_dct['safety_measures'] = 1

    location = 'Muenster'
    rec = Recommendation(user_input_dct, location)
    first_rec = rec.give_recommendation()
    print(len(first_rec))


    # filename = 'model_93'
    
    # cwd = os.getcwd()
    # print(cwd)

    # try:
    #     with open('restaurants/data/{}.pickle'.format(filename), 'rb') as fin:
    #         X = pickle.load(fin)
    #         print('Dataset loaded')
    # except FileNotFoundError:
    #     print('File with saved dataset not found')
    # return X


# if __name__== "__main__":
#     main()