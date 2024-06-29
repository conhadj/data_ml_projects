# Core Pkgs
import streamlit as st 
import os
import base64

# Time Pkg
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

# Templates
file_name = 'yourdocument' + timestr + '.txt'
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


# EDA Pkgs
import pandas as pd 
import numpy as np 
import time,json

# Data Viz Pkg
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")
import seaborn as sns 


# ML Packages
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer


# ML Packages For Vectorization of Text For Feature Extraction
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

import streamlit as st
import pandas as pd
import json


def writetofile(text,file_name):
	with open(os.path.join('downloads',file_name),'w') as f:
		f.write(text)

def download_file():
	file_name = "model_results.json"
	with open(os.path.join('downloads', file_name), 'r') as f:
		result_to_file = f.read()
    
	b64 = base64.b64encode(result_to_file.encode()).decode()
	href = f'<a href="data:file/json;base64,{b64}" download="{file_name}">Download {file_name}</a>'
	st.markdown(href, unsafe_allow_html=True)

# Sampling the dataset if it's too large
def sample_dataframe(df, max_samples=100000):
    if len(df) > max_samples:
        return df.sample(n=max_samples, random_state=42)
    else:
        return df

def main():
	"""Semi Automated ML App with Streamlit """

	activities = ["EDA","Plots","Model Building","About"]	
	choice = st.sidebar.selectbox("Select Activities",activities)

	if choice == 'EDA':
		st.subheader("Exploratory Data Analysis")

		data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
		if data is not None:
			df = pd.read_csv(data)
			st.dataframe(df.head())

			if st.checkbox("Show Shape"):
				st.write(df.shape)

			if st.checkbox("Show Columns"):
				all_columns = df.columns.to_list()  # Initialize all_columns here
				st.write(all_columns)

			if st.checkbox("Summary"):
				st.write(df.describe())

			if st.checkbox("Show Selected Columns"):
				if 'all_columns' not in locals():  # Check if all_columns is initialized
					st.warning("Please select 'Show Columns' first to initialize column list.")
				else:
					selected_columns = st.multiselect("Select Columns", all_columns)
					new_df = df[selected_columns]
					st.dataframe(new_df)

			if st.checkbox("Show Value Counts"):
				st.write(df.iloc[:,-1].value_counts())

			if st.checkbox("Correlation Plot(Matplotlib)"):
				numeric_df = df.select_dtypes(include='number')  # Select only numeric columns
				fig, ax = plt.subplots()
				ax.matshow(numeric_df.corr())
				plt.xticks(range(len(numeric_df.columns)), numeric_df.columns, rotation=90)
				plt.yticks(range(len(numeric_df.columns)), numeric_df.columns)
				st.pyplot(fig)

			if st.checkbox("Correlation Plot(Seaborn)"):
				import seaborn as sns
				numeric_df = df.select_dtypes(include='number')  # Select only numeric columns
				fig, ax = plt.subplots()
				sns.heatmap(numeric_df.corr(), annot=True, ax=ax)
				st.pyplot(fig)

			if st.checkbox("Pie Plot"):
				all_columns = df.columns.to_list()
				column_to_plot = st.selectbox("Select 1 Column", all_columns)

				if df[column_to_plot].dtype == 'object':
					if df[column_to_plot].nunique() <= 30:
						# Plot pie chart
						fig, ax = plt.subplots()
						pie_data = df[column_to_plot].value_counts()
						ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=140)
						ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
						st.pyplot(fig)
					else:
						# Too many categories, display as a table
						st.warning("Selected column has more than 30 categories. Displaying a table instead.")
						value_counts = df[column_to_plot].value_counts().reset_index()
						value_counts.columns = [column_to_plot, 'Count']
						st.dataframe(value_counts)
				else:
					st.write("Selected column is not categorical. Please select a categorical column.")


	elif choice == 'Plots':
		st.subheader("Data Visualization")
		data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
		if data is not None:
			df = pd.read_csv(data)
			st.dataframe(df.head())

			if st.checkbox("Show Value Counts"):
				fig, ax = plt.subplots()
				df.iloc[:, -1].value_counts().plot(kind='bar', ax=ax)
				st.pyplot(fig)
	        
			# Customizable Plot
			all_columns_names = df.columns.tolist()
			type_of_plot = st.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"])
			selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

			if st.button("Generate Plot"):

				if type_of_plot in ["area", "bar", "line"]:
					cust_data = df[selected_columns_names]
					st.success(f"Generating Customizable Plot of {type_of_plot} for {selected_columns_names}")
					if type_of_plot == 'area':
						st.area_chart(cust_data)
					elif type_of_plot == 'bar':
						st.bar_chart(cust_data)
					elif type_of_plot == 'line':
						st.line_chart(cust_data)
				else:
					# Check if the selected columns are numeric for histograms, kde, and box plots
					numeric_columns = df[selected_columns_names].select_dtypes(include='number').columns.tolist()
					if not numeric_columns:
						st.error("No numeric columns selected. Please select at least one numeric column for the chosen plot type.")
					else:
						st.success(f"Generating Customizable Plot of {type_of_plot} for {numeric_columns}")
						fig, ax = plt.subplots()
						df[numeric_columns].plot(kind=type_of_plot, ax=ax)
						st.pyplot(fig)


	elif choice == 'Model Building':

		st.subheader("Building ML Models")
		data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
		
		if data is not None:
			df = pd.read_csv(data)
			st.dataframe(df.head())

			# Sample the dataframe if it's too large
			df = sample_dataframe(df)

			# Select output column (Y)
			output_col = st.selectbox("Select Output Column", df.columns)

			# Encode categorical columns if they are selected as features
			categorical_cols = [col for col in df.columns if df[col].dtype == 'object']
			encoder = LabelEncoder()
			if output_col in categorical_cols:
				df[output_col] = encoder.fit_transform(df[output_col])

			# Handle missing values
			missing_info = df.isnull().sum()
			columns_with_missing = missing_info[missing_info > 0].index.tolist()
			if columns_with_missing:
				st.write("Columns with missing values and the count of missing values:")
				st.write(missing_info[missing_info > 0])

				numeric_cols = df.select_dtypes(include='number').columns
				categorical_cols = df.select_dtypes(include='object').columns

				num_imputer = SimpleImputer(strategy='mean')
				cat_imputer = SimpleImputer(strategy='most_frequent')

				df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])
				df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])

				st.write(f"Missing values were handled: Numeric columns were filled with mean values, and categorical columns were filled with the most frequent values.")


			# Model Building
			X = df.drop(columns=[output_col])
			Y = df[output_col]
	        
			seed = 30
			
			# Determine output type
			if df[output_col].dtype == 'object':
				output_type = 'Categorical'
			else:
				unique_values = df[output_col].nunique()
				if unique_values == 2:
					output_type = 'Numerical Binary'
				elif unique_values > 2:
					output_type = 'Numerical Continuous'
				else:
					st.warning("Unable to determine the output type. Please check the data.")

			st.write(f"Output Type: {output_type}")

			# Define appropriate models based on output type
			if output_type == 'Numerical Binary':
				models = [
					('Logistic Regression', LogisticRegression()),
					('K-Nearest Neighbors', KNeighborsClassifier()),
					('Support Vector Machine', SVC())
				]
				removed_models = [
					('Linear Discriminant Analysis', 'Not suitable for binary output'),
					('Decision Tree', 'Not suitable for binary output'),
					('Gaussian Naive Bayes', 'Not suitable for binary output'),
					('Random Forest', 'Not suitable for binary output')
				]
			elif output_type == 'Numerical Multiclass':
				models = [
					('Logistic Regression', LogisticRegression()),
					('Linear Discriminant Analysis', LinearDiscriminantAnalysis()),
					('K-Nearest Neighbors', KNeighborsClassifier()),
					('Decision Tree', DecisionTreeClassifier()),
					('Gaussian Naive Bayes', GaussianNB()),
					('Support Vector Machine', SVC()),
					('Random Forest', RandomForestClassifier())
				]
				removed_models = []
			elif output_type == 'Numerical Continuous':
				models = [
					('Linear Regression', LinearRegression()),
					('Polynomial Regression', PolynomialFeatures()),
					('Support Vector Regression', SVR()),
					('Decision Tree Regression', DecisionTreeRegressor()),
					('Random Forest Regression', RandomForestRegressor()),
					('Gradient Boosting Regression', GradientBoostingRegressor()),
					('K-Nearest Neighbors Regression', KNeighborsRegressor())
				]
				removed_models = [
					('Logistic Regression', 'Not suitable for continuous output'),
					('Linear Discriminant Analysis', 'Not suitable for continuous output'),
					('K-Nearest Neighbors', 'Not suitable for continuous output'),
					('Decision Tree', 'Not suitable for continuous output'),
					('Gaussian Naive Bayes', 'Not suitable for continuous output')
				]
			else:  # Categorical output
				models = [
					('Linear Discriminant Analysis', LinearDiscriminantAnalysis()),
					('K-Nearest Neighbors', KNeighborsClassifier()),
					('Decision Tree', DecisionTreeClassifier()),
					('Gaussian Naive Bayes', GaussianNB()),
					('Support Vector Machine', SVC()),
					('Random Forest', RandomForestClassifier())
				]
				removed_models = [
					('Logistic Regression', 'Not suitable for categorical output')
				]

			# Print appropriate and removed models
			st.write("Appropriate Models:")
			for model_name, _ in models:
				st.write(f"- {model_name}")

			if removed_models:
				st.write("Models Removed:")
				for model_name, reason in removed_models:
					st.write(f"- {model_name}: {reason}")

			model_names = []
			model_mean = []
			model_std = []
			all_models = []
			scoring = 'accuracy'

			# Initialize progress bar
			progress_bar = st.progress(0)

			total_models = len(models)
	        
			for i, (name, model) in enumerate(models):
				try:
					kfold = KFold(n_splits=10)
					cv_results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
					model_names.append(name)
					model_mean.append(cv_results.mean())
					model_std.append(cv_results.std())

					accuracy_results = {"model name": name, "model_accuracy": cv_results.mean(), "standard deviation": cv_results.std()}
					all_models.append(accuracy_results)

					# Update the progress bar
					progress_bar.progress((i + 1) / total_models)

				except ValueError as e:
					st.error(f"Error occurred for model {name}: {str(e)}")
					st.warning(f"Skipping model {name} due to the error.")

			# After loop completes, clear the progress bar
			progress_bar.empty()

			# Display metrics as table
			if st.checkbox("Metrics As Table"):
				st.dataframe(pd.DataFrame(zip(model_names, model_mean, model_std), columns=["Algorithm", "Mean of Accuracy", "Std"]))

			# Display metrics as JSON
			if st.checkbox("Metrics As JSON"):
				st.json(all_models)

			# Save results button
			if st.button("Save Model Results"):
				result_to_file = json.dumps(all_models)
				file_name = "model_results.json"
				writetofile(result_to_file, file_name)
				st.info(f"Saved Result As: {file_name}")
				download_file()


	elif choice == 'About':
		st.subheader("About")
		st.write("Constantinos Hadjigregoriou")
		st.write("constantinos.hadjigregoriou@outlook.com")





if __name__ == '__main__':
	main()