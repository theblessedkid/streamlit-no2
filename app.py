import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from api_funcs import get_kanye_quote, get_nice_qoute

plt.rcParams.update({'font.size': 22})

"# My first attempt at a streamlit app"

author, quote = get_nice_qoute()

st.sidebar.write(f'>{quote}')
st.sidebar.write(f'*{author}*')


color_list = ['#c23616',
              '#8c7ae6',
              '#dcdde1',
              '#fbc531',
              '#2f3640',
              '#697A55',
              '#8399B3',
              '#C4AA88']


@st.cache(persist=True)
def load_data_from_url(url):
    """

    Load csv data from URL into a pandas dataframe.

    Args:
        url (string): a URL pointing to a csv file

    Returns:
        Dataframe: pandas dataframe

    Raises:
        Exception: None

    """
    dataframe = pd.read_csv(url)
    try:
        dataframe["SicCodes"].fillna("", inplace=True)
        dataframe.rename(columns={'DiffMeanHourlyPercent': 'Difference in Mean Pay between Men and Women (%)',
                                  'DiffMedianHourlyPercent': 'Difference in Median Pay between Men and Women (%)',
                                  'DiffMeanBonusPercent': 'Difference in Mean Bonus between Men and Women (%)',
                                  'DiffMedianBonusPercent': 'Difference in Median Bonus between Men and Women (%)',
                                  'MaleBonusPercent': 'Bonus recieved by Men (%)*',
                                  'FemaleBonusPercent': 'Bonus recieved by Women (%)',
                                  'MaleLowerQuartile': 'Men in the Lower Salary Quartile (%)',
                                  'FemaleLowerQuartile': 'Women in the Lower Salary Quartile (%)',
                                  'MaleLowerMiddleQuartile': 'Men in the Lower Middle Salary Quartile (%)',
                                  'FemaleLowerMiddleQuartile': 'Women in the Lower Middle Salary Quartile (%)',
                                  'MaleUpperMiddleQuartile': 'Men in the Upper Middle Salary Quartile (%)',
                                  'FemaleUpperMiddleQuartile': 'Women in the Upper Middle Salary Quartile (%)',
                                  'MaleTopQuartile': 'Men in the Top Salary Quartile (%)',
                                  'FemaleTopQuartile': 'Women in the Top Salary Quartile (%)'},
                         inplace=True)
    except:
        pass
    return dataframe



# def plot_hist(dataframe, metric, color, label):
#     """ """
#
#
#
#     fig, ax = plt.subplots()
#     ax.hist(dataframe[metric], bins=200)
#
#     plt.axvline(dataframe.describe().at['mean', metric],
#                 color=color, label=label)
#
#     ax.set_xlim(-50, 70)
#
#     ax.set_xlabel(option)
#     return None


def plot_top_10(metric, filtered_df):
    """
    Create a bar chart for the top 20 of a given metric in dataframe.

    Args:
        metric (string): String of a float column in the given dataframe
        filtered_df (dataframe): A pandas dataframe (filtered to allow for comparison)

    Returns:
        None

    Raises:
        Exception: None

    """
    filtered_df.sort_values(by=metric, ascending=False, inplace=True)

    top20 = filtered_df.head(10).sort_values(by=metric)
    top20["EmployerName"] = top20["EmployerName"].str.title()

    fig1 = plt.figure(figsize=(20, 14))
    plt.barh(y='EmployerName', width=metric, data=top20)

    plt.axvline(filtered_df.describe().at['mean', metric],
                label=f"average {metric} across sector", color=color_list[4],
                linewidth=10, alpha=0.7)
    plt.axvline(df.describe().at['mean', metric],
                label=f"UK average {metric} (all sectors)", color=color_list[7],
                linewidth=10, alpha=0.7)
    plt.legend(bbox_to_anchor=(0, 1, 1, 0),loc="lower left")
    plt.box(False)
    plt.ylabel("")
    plt.tight_layout()

    for i, v in enumerate(top20[metric]):
        plt.text(v + 0.1, i - 0.1, str(v))

    st.pyplot(fig1)



# Loading data
url_dict = {'2017': "https://gender-pay-gap.service.gov.uk/viewing/download-data/2017",
            '2018': "https://gender-pay-gap.service.gov.uk/viewing/download-data/2018",
            '2019': "https://gender-pay-gap.service.gov.uk/viewing/download-data/2019",
            '2020': "https://gender-pay-gap.service.gov.uk/viewing/download-data/2020"}

year = st.sidebar.radio(
    "Year",
    ('2017', '2018', '2019', '2020'))

URL = url_dict[year]
df = load_data_from_url(URL)

# Dataframe split by location
london = df[df["Address"].str.contains("London") == True]
liverpool = df[df["Address"].str.contains("Liverpool")
               | df["Address"].str.contains("Merseyside")]
midlands = df[df["Address"].str.contains("Coventry")
              | df["Address"].str.contains("Birmingham")
              | df["Address"].str.contains("Oxfordshire")
              | df["Address"].str.contains("Nottinghamshire")
              | df["Address"].str.contains("Cambridgeshire")
              | df["Address"].str.contains("Staffordshire")
              | df["Address"].str.contains("Hertfordshire")
              | df["Address"].str.contains("West Midlands")]


# Dataframe split by sector
football = df[df["EmployerName"].str.contains("FOOTBALL")
              | df["EmployerName"].str.contains("Football")]
bank = df[df['EmployerName'].str.contains("BANK")
          | (df["EmployerName"].str.contains("Bank") &
             (~df["EmployerName"].str.contains("University")))]
nhs = df[df['EmployerName'].str.contains('NHS') == True]
university = df[df["SicCodes"].str.contains("85421") |
                (df["EmployerName"].str.contains("University") &
                 (~df["EmployerName"].str.contains("Hospital") &
                  ~df["EmployerName"].str.contains("Union", case=False)))]


st.write(f"The data has {df.shape[1]} features from {df.shape[0]} employers. It looks like this.")
if st.checkbox('Show dataframe'):
    st.dataframe(df)

'### Plotting difference in pay across all employers for different regions'
metrics = [col for col in df.columns if df[col].dtype == float]
option = st.selectbox('Difference: ', metrics)

ax = plt.figure(figsize=(20, 14))
plt.hist(df[option], bins=200)
plt.hist(liverpool[option], bins=200)
plt.hist(london[option], bins=200)
plt.hist(midlands[option], bins=200)

plt.axvline(df.describe().at['mean', option],
            color=color_list[3], label='UK mean',
            linewidth=10, alpha=0.7)
plt.axvline(london.describe().at['mean', option],
            color=color_list[2], label='London mean',
            linewidth=10, alpha=0.7)
plt.axvline(liverpool.describe().at['mean', option],
            color=color_list[1], label='Liverpool mean',
            linewidth=10, alpha=0.7)
plt.axvline(midlands.describe().at['mean', option],
            color=color_list[0], label='Midlands mean',
            linewidth=10, alpha=0.7)

plt.xlim(-50, 70)
plt.xlabel(option)

plt.ylabel("Number of Employers")
plt.title('')
plt.legend()
st.pyplot(ax)

'### The largest gaps in certain sectors'

df_dict = {'Football': football,
           'Banking': bank,
           'NHS': nhs,
           'University': university}

sector = st.radio(
    "Sector",
    ('Football', 'University', 'NHS', 'Banking'))

plot_top_10(option, df_dict[sector])

st.sidebar.write('The source for this data can be found [here](https://gender-pay-gap.service.gov.uk/). The code is adapted from [this notebook](https://colab.research.google.com/drive/1pA7IfUcZjG64pAn5Dw5bUsnYdo1KNXZ2?usp=sharing), provided by the wonderful HiPy program.')
