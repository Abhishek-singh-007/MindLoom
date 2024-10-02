{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "9jdjU2tPS3TV"
      },
      "source": [
        "# Loading data and preliminary analysis"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Install dependencies \n",
        "\n",
        "%pip install -r '../requirements.txt'\n",
        "\n",
        "import nltk \n",
        "\n",
        "nltk.download('punkt') \n",
        "nltk.download('averaged_perceptron_tagger') \n",
        "\n",
        "# Set paths \n",
        "\n",
        "path_to_csv = '../Dataset/mentalhealth.csv'"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "id": "C4ZJBL6Y08Me"
      },
      "outputs": [],
      "source": [
        "import pandas as pd\n",
        "import nltk \n",
        "import numpy as np\n",
        "import re\n",
        "\n",
        "from nltk.stem import wordnet                                  # to perform lemmitization\n",
        "from sklearn.feature_extraction.text import CountVectorizer    # to perform bow\n",
        "from sklearn.feature_extraction.text import TfidfVectorizer    # to perform tfidf\n",
        "from nltk import pos_tag                                       # for parts of speech\n",
        "from sklearn.metrics import pairwise_distances                 # to perfrom cosine similarity\n",
        "from nltk import word_tokenize                                 # to create tokens\n",
        "from nltk.corpus import stopwords                              # for stop words"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 3,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 203
        },
        "id": "Iibn50pd1mab",
        "outputId": "583e8d39-2c2b-42f9-e3dd-2b3656fadad4"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Question_ID</th>\n",
              "      <th>Questions</th>\n",
              "      <th>Answers</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>1590140</td>\n",
              "      <td>What does it mean to have a mental illness?</td>\n",
              "      <td>Mental illnesses are health conditions that di...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>2110618</td>\n",
              "      <td>Who does mental illness affect?</td>\n",
              "      <td>Mental illness does can affect anyone, regardl...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>9434130</td>\n",
              "      <td>What are some of the warning signs of mental i...</td>\n",
              "      <td>Symptoms of mental health disorders vary depen...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>7657263</td>\n",
              "      <td>Can people with mental illness recover?</td>\n",
              "      <td>When healing from mental illness, early identi...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>1619387</td>\n",
              "      <td>What should I do if I know someone who appears...</td>\n",
              "      <td>We encourage those with symptoms to talk to th...</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "   Question_ID                                          Questions  \\\n",
              "0      1590140        What does it mean to have a mental illness?   \n",
              "1      2110618                    Who does mental illness affect?   \n",
              "2      9434130  What are some of the warning signs of mental i...   \n",
              "3      7657263            Can people with mental illness recover?   \n",
              "4      1619387  What should I do if I know someone who appears...   \n",
              "\n",
              "                                             Answers  \n",
              "0  Mental illnesses are health conditions that di...  \n",
              "1  Mental illness does can affect anyone, regardl...  \n",
              "2  Symptoms of mental health disorders vary depen...  \n",
              "3  When healing from mental illness, early identi...  \n",
              "4  We encourage those with symptoms to talk to th...  "
            ]
          },
          "execution_count": 3,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df = pd.read_csv(path_to_csv, nrows = 20)\n",
        "df.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 4,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "kmGaGT3mTPAw",
        "outputId": "19240647-6bda-46b6-f346-62501e3d0844"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "Question_ID    0\n",
              "Questions      0\n",
              "Answers        0\n",
              "dtype: int64"
            ]
          },
          "execution_count": 4,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df.isnull().sum()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "hh7lUX72TSO9"
      },
      "source": [
        "# Clean data using NLTK\n",
        "\n",
        "\n",
        "\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 5,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "DM0bO0b03dD2",
        "outputId": "611344d0-9c7c-4606-877a-48761278d876"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "['tell', 'me', 'about', 'your', 'personality']\n"
          ]
        }
      ],
      "source": [
        "s = 'tell me about your personality'\n",
        "words = word_tokenize(s)                    # tokenize words\n",
        "print(words)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 6,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 71
        },
        "id": "82lHgG0d3rBH",
        "outputId": "3f158b02-f7f5-4656-dbe4-cbe0c8713180"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "'absorb'"
            ]
          },
          "execution_count": 6,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "# nltk.download('wordnet')                    # uncomment if running the cell for the first time\n",
        "lemma = wordnet.WordNetLemmatizer()         \n",
        "lemma.lemmatize('absorbed', pos = 'v')        # lemmatize words"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 7,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "jEw94aKZ3zvz",
        "outputId": "68c7fa09-ed14-4388-d8e9-5765567786b8"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "[('tell', 'VB'),\n",
              " ('me', 'PRP'),\n",
              " ('about', 'IN'),\n",
              " ('your', 'PRP$'),\n",
              " ('personality', 'NN')]"
            ]
          },
          "execution_count": 7,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "pos_tag(nltk.word_tokenize(s),tagset = None)       # returns the parts of speech of every word"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 8,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "T-BDv4Yj4Ngc",
        "outputId": "acd49f9f-0e2d-4e8f-824d-16f1b5ba5c1f"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', \"you're\", \"you've\", \"you'll\", \"you'd\", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', \"she's\", 'her', 'hers', 'herself', 'it', \"it's\", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', \"that'll\", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', \"don't\", 'should', \"should've\", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', \"aren't\", 'couldn', \"couldn't\", 'didn', \"didn't\", 'doesn', \"doesn't\", 'hadn', \"hadn't\", 'hasn', \"hasn't\", 'haven', \"haven't\", 'isn', \"isn't\", 'ma', 'mightn', \"mightn't\", 'mustn', \"mustn't\", 'needn', \"needn't\", 'shan', \"shan't\", 'shouldn', \"shouldn't\", 'wasn', \"wasn't\", 'weren', \"weren't\", 'won', \"won't\", 'wouldn', \"wouldn't\"]\n"
          ]
        },
        {
          "name": "stderr",
          "output_type": "stream",
          "text": [
            "[nltk_data] Downloading package stopwords to\n",
            "[nltk_data]     /Users/anuradha.pandey/nltk_data...\n",
            "[nltk_data]   Package stopwords is already up-to-date!\n"
          ]
        }
      ],
      "source": [
        " nltk.download('stopwords')            # uncomment if running the cell for the first time\n",
        "\n",
        "stop = stopwords.words('english')\n",
        "print(stop)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 9,
      "metadata": {
        "id": "QmrI6JPL39US"
      },
      "outputs": [],
      "source": [
        "# function that performs text normalization steps and returns the lemmatized tokens as a sentence\n",
        "\n",
        "def text_normalization(text):\n",
        "    text = str(text).lower()                        # text to lower case\n",
        "    spl_char_text = re.sub(r'[^ a-z]','',text)      # removing special characters\n",
        "    tokens = nltk.word_tokenize(spl_char_text)      # word tokenizing\n",
        "    lema = wordnet.WordNetLemmatizer()              # intializing lemmatization\n",
        "    tags_list = pos_tag(tokens,tagset=None)         # parts of speech\n",
        "    lema_words = []                                 # empty list \n",
        "    for token,pos_token in tags_list:               # lemmatize according to POS\n",
        "        if pos_token.startswith('V'):               # Verb\n",
        "            pos_val = 'v'\n",
        "        elif pos_token.startswith('J'):             # Adjective\n",
        "            pos_val = 'a'\n",
        "        elif pos_token.startswith('R'):             # Adverb\n",
        "            pos_val = 'r'\n",
        "        else:\n",
        "            pos_val = 'n'                           # Noun\n",
        "        lema_token = lema.lemmatize(token,pos_val)\n",
        "\n",
        "        if lema_token in stop: \n",
        "          lema_words.append(lema_token)             # appending the lemmatized token into a list\n",
        "    \n",
        "    return \" \".join(lema_words) "
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 10,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "id": "jyvzid3c4A2x",
        "outputId": "29b0810a-2849-4fc7-9a72-3ea416432385"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "'you some about me'"
            ]
          },
          "execution_count": 10,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "text_normalization('telling you some stuffs about me')  # example"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 11,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 237
        },
        "id": "CXPVFcd64EIo",
        "outputId": "ab3c646a-ceef-47d8-c2b1-b51271ea48ff"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Question_ID</th>\n",
              "      <th>Questions</th>\n",
              "      <th>Answers</th>\n",
              "      <th>lemmatized_text</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>1590140</td>\n",
              "      <td>What does it mean to have a mental illness?</td>\n",
              "      <td>Mental illnesses are health conditions that di...</td>\n",
              "      <td>what do it to have a</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>2110618</td>\n",
              "      <td>Who does mental illness affect?</td>\n",
              "      <td>Mental illness does can affect anyone, regardl...</td>\n",
              "      <td>who do</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>9434130</td>\n",
              "      <td>What are some of the warning signs of mental i...</td>\n",
              "      <td>Symptoms of mental health disorders vary depen...</td>\n",
              "      <td>what be some of the of</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>7657263</td>\n",
              "      <td>Can people with mental illness recover?</td>\n",
              "      <td>When healing from mental illness, early identi...</td>\n",
              "      <td>can with</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>1619387</td>\n",
              "      <td>What should I do if I know someone who appears...</td>\n",
              "      <td>We encourage those with symptoms to talk to th...</td>\n",
              "      <td>what should i do if i who to have the of a</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "   Question_ID                                          Questions  \\\n",
              "0      1590140        What does it mean to have a mental illness?   \n",
              "1      2110618                    Who does mental illness affect?   \n",
              "2      9434130  What are some of the warning signs of mental i...   \n",
              "3      7657263            Can people with mental illness recover?   \n",
              "4      1619387  What should I do if I know someone who appears...   \n",
              "\n",
              "                                             Answers  \\\n",
              "0  Mental illnesses are health conditions that di...   \n",
              "1  Mental illness does can affect anyone, regardl...   \n",
              "2  Symptoms of mental health disorders vary depen...   \n",
              "3  When healing from mental illness, early identi...   \n",
              "4  We encourage those with symptoms to talk to th...   \n",
              "\n",
              "                              lemmatized_text  \n",
              "0                        what do it to have a  \n",
              "1                                      who do  \n",
              "2                      what be some of the of  \n",
              "3                                    can with  \n",
              "4  what should i do if i who to have the of a  "
            ]
          },
          "execution_count": 11,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df['lemmatized_text'] = df['Questions'].apply(text_normalization)   # clean text\n",
        "df.head(5)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 12,
      "metadata": {
        "id": "GRpLiLLR4T58"
      },
      "outputs": [],
      "source": [
        "cv = CountVectorizer()                                  # intializing the count vectorizer\n",
        "X = cv.fit_transform(df['lemmatized_text']).toarray()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 13,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 223
        },
        "id": "HKDdHYo04XG9",
        "outputId": "caf8de83-10c9-47c7-bf7a-4178db9a77e0"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>about</th>\n",
              "      <th>after</th>\n",
              "      <th>and</th>\n",
              "      <th>be</th>\n",
              "      <th>before</th>\n",
              "      <th>between</th>\n",
              "      <th>can</th>\n",
              "      <th>do</th>\n",
              "      <th>for</th>\n",
              "      <th>have</th>\n",
              "      <th>...</th>\n",
              "      <th>or</th>\n",
              "      <th>should</th>\n",
              "      <th>some</th>\n",
              "      <th>the</th>\n",
              "      <th>this</th>\n",
              "      <th>to</th>\n",
              "      <th>what</th>\n",
              "      <th>where</th>\n",
              "      <th>who</th>\n",
              "      <th>with</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>...</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "      <td>1</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>5 rows × 27 columns</p>\n",
              "</div>"
            ],
            "text/plain": [
              "   about  after  and  be  before  between  can  do  for  have  ...  or  \\\n",
              "0      0      0    0   0       0        0    0   1    0     1  ...   0   \n",
              "1      0      0    0   0       0        0    0   1    0     0  ...   0   \n",
              "2      0      0    0   1       0        0    0   0    0     0  ...   0   \n",
              "3      0      0    0   0       0        0    1   0    0     0  ...   0   \n",
              "4      0      0    0   0       0        0    0   1    0     1  ...   0   \n",
              "\n",
              "   should  some  the  this  to  what  where  who  with  \n",
              "0       0     0    0     0   1     1      0    0     0  \n",
              "1       0     0    0     0   0     0      0    1     0  \n",
              "2       0     1    1     0   0     1      0    0     0  \n",
              "3       0     0    0     0   0     0      0    0     1  \n",
              "4       1     0    1     0   1     1      0    1     0  \n",
              "\n",
              "[5 rows x 27 columns]"
            ]
          },
          "execution_count": 13,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "# returns all the unique word from data \n",
        "\n",
        "features = cv.get_feature_names_out()\n",
        "df_bow = pd.DataFrame(X, columns = features)\n",
        "df_bow.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 14,
      "metadata": {
        "id": "CMh7mfw0PH1q"
      },
      "outputs": [],
      "source": [
        "Question = 'What treatment options are available'                           # example"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 15,
      "metadata": {
        "id": "ErwQk4Jf4iSY"
      },
      "outputs": [],
      "source": [
        "Question_lemma = text_normalization(Question)                               # clean text\n",
        "Question_bow = cv.transform([Question_lemma]).toarray()                     # applying bow"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "ZshENmwyV9I9"
      },
      "source": [
        "# Cosine similarity"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 16,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "SWylluoYA6O0",
        "outputId": "d68d6d22-7971-4f83-8567-6ff231a8ccc7"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "array([[0.31622777],\n",
              "       [0.        ],\n",
              "       [0.5       ],\n",
              "       [0.        ],\n",
              "       [0.23570226],\n",
              "       [0.        ],\n",
              "       [1.        ],\n",
              "       [0.31622777],\n",
              "       [0.70710678],\n",
              "       [0.        ],\n",
              "       [0.31622777],\n",
              "       [0.        ],\n",
              "       [0.40824829],\n",
              "       [0.25      ],\n",
              "       [0.        ],\n",
              "       [0.        ],\n",
              "       [0.        ],\n",
              "       [0.70710678],\n",
              "       [0.        ],\n",
              "       [0.        ]])"
            ]
          },
          "execution_count": 16,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "# cosine similarity for the above question we considered.\n",
        "\n",
        "cosine_value = 1- pairwise_distances(df_bow, Question_bow, metric = 'cosine' )\n",
        "(cosine_value)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 17,
      "metadata": {
        "id": "9BlKaaezA8s_"
      },
      "outputs": [],
      "source": [
        "df['similarity_bow'] = cosine_value                                         # create cosine value as a new column"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 18,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 665
        },
        "id": "ja0_jD4iA_NW",
        "outputId": "4dcbb27b-2b02-4408-ed4a-5f6100e10acb"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Answers</th>\n",
              "      <th>similarity_bow</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Mental illnesses are health conditions that di...</td>\n",
              "      <td>0.316228</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>Mental illness does can affect anyone, regardl...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Symptoms of mental health disorders vary depen...</td>\n",
              "      <td>0.500000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>When healing from mental illness, early identi...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>We encourage those with symptoms to talk to th...</td>\n",
              "      <td>0.235702</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>Feeling comfortable with the professional you ...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>Different treatment options are available for ...</td>\n",
              "      <td>1.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>It is important to be as involved and engaged ...</td>\n",
              "      <td>0.316228</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>0.707107</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>Feeling comfortable with the professional you ...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>10</th>\n",
              "      <td>It is important to continue involvement in the...</td>\n",
              "      <td>0.316228</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>11</th>\n",
              "      <td>family member, friend, clergy, healthcare prov...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>12</th>\n",
              "      <td>The best source of information regarding medic...</td>\n",
              "      <td>0.408248</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13</th>\n",
              "      <td>Create a plan for switching to a different tre...</td>\n",
              "      <td>0.250000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>14</th>\n",
              "      <td>Visit Healthfinder.gov to learn more.</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>15</th>\n",
              "      <td>Several different types of treatment and thera...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>16</th>\n",
              "      <td>Mental health conditions are often treated wit...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>17</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>0.707107</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>18</th>\n",
              "      <td>Many people find peer support a helpful tool t...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>19</th>\n",
              "      <td>Inpatient care can help people stabilize on ne...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "                                              Answers  similarity_bow\n",
              "0   Mental illnesses are health conditions that di...        0.316228\n",
              "1   Mental illness does can affect anyone, regardl...        0.000000\n",
              "2   Symptoms of mental health disorders vary depen...        0.500000\n",
              "3   When healing from mental illness, early identi...        0.000000\n",
              "4   We encourage those with symptoms to talk to th...        0.235702\n",
              "5   Feeling comfortable with the professional you ...        0.000000\n",
              "6   Different treatment options are available for ...        1.000000\n",
              "7   It is important to be as involved and engaged ...        0.316228\n",
              "8   There are many types of mental health professi...        0.707107\n",
              "9   Feeling comfortable with the professional you ...        0.000000\n",
              "10  It is important to continue involvement in the...        0.316228\n",
              "11  family member, friend, clergy, healthcare prov...        0.000000\n",
              "12  The best source of information regarding medic...        0.408248\n",
              "13  Create a plan for switching to a different tre...        0.250000\n",
              "14              Visit Healthfinder.gov to learn more.        0.000000\n",
              "15  Several different types of treatment and thera...        0.000000\n",
              "16  Mental health conditions are often treated wit...        0.000000\n",
              "17  There are many types of mental health professi...        0.707107\n",
              "18  Many people find peer support a helpful tool t...        0.000000\n",
              "19  Inpatient care can help people stabilize on ne...        0.000000"
            ]
          },
          "execution_count": 18,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "simiscores = pd.DataFrame(df, columns=['Answers','similarity_bow'])         # taking similarity value of responses for the question we took\n",
        "simiscores"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 19,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 203
        },
        "id": "8NwdGoDGBRwi",
        "outputId": "7387fc5a-ec4a-4bd1-d35a-4cae4b3893a1"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Answers</th>\n",
              "      <th>similarity_bow</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>Different treatment options are available for ...</td>\n",
              "      <td>1.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>17</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>0.707107</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>0.707107</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Symptoms of mental health disorders vary depen...</td>\n",
              "      <td>0.500000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>12</th>\n",
              "      <td>The best source of information regarding medic...</td>\n",
              "      <td>0.408248</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "                                              Answers  similarity_bow\n",
              "6   Different treatment options are available for ...        1.000000\n",
              "17  There are many types of mental health professi...        0.707107\n",
              "8   There are many types of mental health professi...        0.707107\n",
              "2   Symptoms of mental health disorders vary depen...        0.500000\n",
              "12  The best source of information regarding medic...        0.408248"
            ]
          },
          "execution_count": 19,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "simscoresDescending = simiscores.sort_values(by = 'similarity_bow', ascending=False)          # sorting the values\n",
        "simscoresDescending.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 20,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 357
        },
        "id": "Yt6jgDc5BY-m",
        "outputId": "77d5bb00-be7f-4673-dc65-4a16ab96fe24"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Answers</th>\n",
              "      <th>similarity_bow</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>Different treatment options are available for ...</td>\n",
              "      <td>1.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>17</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>0.707107</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>0.707107</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Symptoms of mental health disorders vary depen...</td>\n",
              "      <td>0.500000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>12</th>\n",
              "      <td>The best source of information regarding medic...</td>\n",
              "      <td>0.408248</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Mental illnesses are health conditions that di...</td>\n",
              "      <td>0.316228</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>It is important to be as involved and engaged ...</td>\n",
              "      <td>0.316228</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>10</th>\n",
              "      <td>It is important to continue involvement in the...</td>\n",
              "      <td>0.316228</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13</th>\n",
              "      <td>Create a plan for switching to a different tre...</td>\n",
              "      <td>0.250000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>We encourage those with symptoms to talk to th...</td>\n",
              "      <td>0.235702</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "                                              Answers  similarity_bow\n",
              "6   Different treatment options are available for ...        1.000000\n",
              "17  There are many types of mental health professi...        0.707107\n",
              "8   There are many types of mental health professi...        0.707107\n",
              "2   Symptoms of mental health disorders vary depen...        0.500000\n",
              "12  The best source of information regarding medic...        0.408248\n",
              "0   Mental illnesses are health conditions that di...        0.316228\n",
              "7   It is important to be as involved and engaged ...        0.316228\n",
              "10  It is important to continue involvement in the...        0.316228\n",
              "13  Create a plan for switching to a different tre...        0.250000\n",
              "4   We encourage those with symptoms to talk to th...        0.235702"
            ]
          },
          "execution_count": 20,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "threshold = 0.1                                                                         # considering the value of smiliarity to be greater than 0.1\n",
        "df_threshold = simscoresDescending[simscoresDescending['similarity_bow'] > threshold] \n",
        "df_threshold"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 21,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "uFgAg8EnBkey",
        "outputId": "8f5764b0-3f9b-4bfe-b684-00dd6407d159"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "6"
            ]
          },
          "execution_count": 21,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "index_value = cosine_value.argmax()         # index number of highest value\n",
        "index_value"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 22,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "id": "IcCqWPu7Bn8I",
        "outputId": "58e18516-71cf-48b7-9120-29ef19669bc0"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "'Different treatment options are available for individuals with mental illness.'"
            ]
          },
          "execution_count": 22,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df['Answers'].loc[index_value]              # The text at the above index becomes the response for the question"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "wG7sF9MaWD27"
      },
      "source": [
        "# Tf-Idf"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 23,
      "metadata": {
        "id": "O3WMQ7YBByib"
      },
      "outputs": [],
      "source": [
        "Question1 = 'What treatment options are available'"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 24,
      "metadata": {
        "id": "yxGhvUqsB96d"
      },
      "outputs": [],
      "source": [
        "# using tf-idf\n",
        "\n",
        "tfidf = TfidfVectorizer()                                             # intializing tf-id \n",
        "x_tfidf = tfidf.fit_transform(df['lemmatized_text']).toarray()        # transforming the data into array"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 25,
      "metadata": {
        "id": "Njbou1tyCAVm"
      },
      "outputs": [],
      "source": [
        "Question_lemma1 = text_normalization(Question1)\n",
        "Question_tfidf = tfidf.transform([Question_lemma1]).toarray()         # applying tf-idf"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 26,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 223
        },
        "id": "10YovQFdCJ1h",
        "outputId": "adf1fd58-a2dc-45ff-8b6f-2f2d7a0c5e75"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>about</th>\n",
              "      <th>after</th>\n",
              "      <th>and</th>\n",
              "      <th>be</th>\n",
              "      <th>before</th>\n",
              "      <th>between</th>\n",
              "      <th>can</th>\n",
              "      <th>do</th>\n",
              "      <th>for</th>\n",
              "      <th>have</th>\n",
              "      <th>...</th>\n",
              "      <th>or</th>\n",
              "      <th>should</th>\n",
              "      <th>some</th>\n",
              "      <th>the</th>\n",
              "      <th>this</th>\n",
              "      <th>to</th>\n",
              "      <th>what</th>\n",
              "      <th>where</th>\n",
              "      <th>who</th>\n",
              "      <th>with</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.392029</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.550307</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.367085</td>\n",
              "      <td>0.325401</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.580211</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.814466</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.321859</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.478821</td>\n",
              "      <td>0.347908</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.248876</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.440977</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.897519</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.282658</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.396779</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.396779</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.327977</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.264673</td>\n",
              "      <td>0.234618</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.396779</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>5 rows × 27 columns</p>\n",
              "</div>"
            ],
            "text/plain": [
              "   about  after  and        be  before  between       can        do  for  \\\n",
              "0    0.0    0.0  0.0  0.000000     0.0      0.0  0.000000  0.392029  0.0   \n",
              "1    0.0    0.0  0.0  0.000000     0.0      0.0  0.000000  0.580211  0.0   \n",
              "2    0.0    0.0  0.0  0.321859     0.0      0.0  0.000000  0.000000  0.0   \n",
              "3    0.0    0.0  0.0  0.000000     0.0      0.0  0.440977  0.000000  0.0   \n",
              "4    0.0    0.0  0.0  0.000000     0.0      0.0  0.000000  0.282658  0.0   \n",
              "\n",
              "       have  ...   or    should      some       the  this        to      what  \\\n",
              "0  0.550307  ...  0.0  0.000000  0.000000  0.000000   0.0  0.367085  0.325401   \n",
              "1  0.000000  ...  0.0  0.000000  0.000000  0.000000   0.0  0.000000  0.000000   \n",
              "2  0.000000  ...  0.0  0.000000  0.478821  0.347908   0.0  0.000000  0.248876   \n",
              "3  0.000000  ...  0.0  0.000000  0.000000  0.000000   0.0  0.000000  0.000000   \n",
              "4  0.396779  ...  0.0  0.396779  0.000000  0.327977   0.0  0.264673  0.234618   \n",
              "\n",
              "   where       who      with  \n",
              "0    0.0  0.000000  0.000000  \n",
              "1    0.0  0.814466  0.000000  \n",
              "2    0.0  0.000000  0.000000  \n",
              "3    0.0  0.000000  0.897519  \n",
              "4    0.0  0.396779  0.000000  \n",
              "\n",
              "[5 rows x 27 columns]"
            ]
          },
          "execution_count": 26,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "# returns all the unique word from data with a score of that word\n",
        "\n",
        "df_tfidf = pd.DataFrame(x_tfidf,columns = tfidf.get_feature_names_out()) \n",
        "df_tfidf.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 27,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "IEAPLV2mCWAY",
        "outputId": "cb74e6eb-7c00-4afd-e571-a191c13bfe72"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "array([[0.19904882],\n",
              "       [0.        ],\n",
              "       [0.40685646],\n",
              "       [0.        ],\n",
              "       [0.14351684],\n",
              "       [0.        ],\n",
              "       [1.        ],\n",
              "       [0.20934186],\n",
              "       [0.56647821],\n",
              "       [0.        ],\n",
              "       [0.20934186],\n",
              "       [0.        ],\n",
              "       [0.22245129],\n",
              "       [0.22913146],\n",
              "       [0.        ],\n",
              "       [0.        ],\n",
              "       [0.        ],\n",
              "       [0.6372619 ],\n",
              "       [0.        ],\n",
              "       [0.        ]])"
            ]
          },
          "execution_count": 27,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "cos = 1-pairwise_distances(df_tfidf,Question_tfidf,metric='cosine')                     # applying cosine similarity\n",
        "cos"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 28,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 665
        },
        "id": "5saQViVjCXng",
        "outputId": "94e722f4-7084-480e-a4ae-6b3f0f8ae340"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Answers</th>\n",
              "      <th>similarity_tfidf</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Mental illnesses are health conditions that di...</td>\n",
              "      <td>0.199049</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>Mental illness does can affect anyone, regardl...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Symptoms of mental health disorders vary depen...</td>\n",
              "      <td>0.406856</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>When healing from mental illness, early identi...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>We encourage those with symptoms to talk to th...</td>\n",
              "      <td>0.143517</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>Feeling comfortable with the professional you ...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>Different treatment options are available for ...</td>\n",
              "      <td>1.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>It is important to be as involved and engaged ...</td>\n",
              "      <td>0.209342</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>0.566478</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>Feeling comfortable with the professional you ...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>10</th>\n",
              "      <td>It is important to continue involvement in the...</td>\n",
              "      <td>0.209342</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>11</th>\n",
              "      <td>family member, friend, clergy, healthcare prov...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>12</th>\n",
              "      <td>The best source of information regarding medic...</td>\n",
              "      <td>0.222451</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13</th>\n",
              "      <td>Create a plan for switching to a different tre...</td>\n",
              "      <td>0.229131</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>14</th>\n",
              "      <td>Visit Healthfinder.gov to learn more.</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>15</th>\n",
              "      <td>Several different types of treatment and thera...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>16</th>\n",
              "      <td>Mental health conditions are often treated wit...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>17</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>0.637262</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>18</th>\n",
              "      <td>Many people find peer support a helpful tool t...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>19</th>\n",
              "      <td>Inpatient care can help people stabilize on ne...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "                                              Answers  similarity_tfidf\n",
              "0   Mental illnesses are health conditions that di...          0.199049\n",
              "1   Mental illness does can affect anyone, regardl...          0.000000\n",
              "2   Symptoms of mental health disorders vary depen...          0.406856\n",
              "3   When healing from mental illness, early identi...          0.000000\n",
              "4   We encourage those with symptoms to talk to th...          0.143517\n",
              "5   Feeling comfortable with the professional you ...          0.000000\n",
              "6   Different treatment options are available for ...          1.000000\n",
              "7   It is important to be as involved and engaged ...          0.209342\n",
              "8   There are many types of mental health professi...          0.566478\n",
              "9   Feeling comfortable with the professional you ...          0.000000\n",
              "10  It is important to continue involvement in the...          0.209342\n",
              "11  family member, friend, clergy, healthcare prov...          0.000000\n",
              "12  The best source of information regarding medic...          0.222451\n",
              "13  Create a plan for switching to a different tre...          0.229131\n",
              "14              Visit Healthfinder.gov to learn more.          0.000000\n",
              "15  Several different types of treatment and thera...          0.000000\n",
              "16  Mental health conditions are often treated wit...          0.000000\n",
              "17  There are many types of mental health professi...          0.637262\n",
              "18  Many people find peer support a helpful tool t...          0.000000\n",
              "19  Inpatient care can help people stabilize on ne...          0.000000"
            ]
          },
          "execution_count": 28,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df['similarity_tfidf'] = cos                                                    # creating a new column \n",
        "df_simi_tfidf = pd.DataFrame(df, columns=['Answers','similarity_tfidf'])        # taking similarity value of responses for the question we took\n",
        "df_simi_tfidf"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 29,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 357
        },
        "id": "f1rs3m98CfR9",
        "outputId": "13c7b88e-ffbf-4095-8e5a-7a5a768400d5"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Answers</th>\n",
              "      <th>similarity_tfidf</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>Different treatment options are available for ...</td>\n",
              "      <td>1.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>17</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>0.637262</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>0.566478</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Symptoms of mental health disorders vary depen...</td>\n",
              "      <td>0.406856</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13</th>\n",
              "      <td>Create a plan for switching to a different tre...</td>\n",
              "      <td>0.229131</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>12</th>\n",
              "      <td>The best source of information regarding medic...</td>\n",
              "      <td>0.222451</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>10</th>\n",
              "      <td>It is important to continue involvement in the...</td>\n",
              "      <td>0.209342</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>It is important to be as involved and engaged ...</td>\n",
              "      <td>0.209342</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Mental illnesses are health conditions that di...</td>\n",
              "      <td>0.199049</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>We encourage those with symptoms to talk to th...</td>\n",
              "      <td>0.143517</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "                                              Answers  similarity_tfidf\n",
              "6   Different treatment options are available for ...          1.000000\n",
              "17  There are many types of mental health professi...          0.637262\n",
              "8   There are many types of mental health professi...          0.566478\n",
              "2   Symptoms of mental health disorders vary depen...          0.406856\n",
              "13  Create a plan for switching to a different tre...          0.229131\n",
              "12  The best source of information regarding medic...          0.222451\n",
              "10  It is important to continue involvement in the...          0.209342\n",
              "7   It is important to be as involved and engaged ...          0.209342\n",
              "0   Mental illnesses are health conditions that di...          0.199049\n",
              "4   We encourage those with symptoms to talk to th...          0.143517"
            ]
          },
          "execution_count": 29,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df_simi_tfidf_sort = df_simi_tfidf.sort_values(by='similarity_tfidf', ascending=False)            # sorting the values\n",
        "df_simi_tfidf_sort.head(10)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 30,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 357
        },
        "id": "Bc3fzoRqCjYC",
        "outputId": "aae31ced-faf3-40e1-fc9a-9ed44db0dc59"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Answers</th>\n",
              "      <th>similarity_tfidf</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>Different treatment options are available for ...</td>\n",
              "      <td>1.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>17</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>0.637262</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>0.566478</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Symptoms of mental health disorders vary depen...</td>\n",
              "      <td>0.406856</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13</th>\n",
              "      <td>Create a plan for switching to a different tre...</td>\n",
              "      <td>0.229131</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>12</th>\n",
              "      <td>The best source of information regarding medic...</td>\n",
              "      <td>0.222451</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>10</th>\n",
              "      <td>It is important to continue involvement in the...</td>\n",
              "      <td>0.209342</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>It is important to be as involved and engaged ...</td>\n",
              "      <td>0.209342</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Mental illnesses are health conditions that di...</td>\n",
              "      <td>0.199049</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>We encourage those with symptoms to talk to th...</td>\n",
              "      <td>0.143517</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "                                              Answers  similarity_tfidf\n",
              "6   Different treatment options are available for ...          1.000000\n",
              "17  There are many types of mental health professi...          0.637262\n",
              "8   There are many types of mental health professi...          0.566478\n",
              "2   Symptoms of mental health disorders vary depen...          0.406856\n",
              "13  Create a plan for switching to a different tre...          0.229131\n",
              "12  The best source of information regarding medic...          0.222451\n",
              "10  It is important to continue involvement in the...          0.209342\n",
              "7   It is important to be as involved and engaged ...          0.209342\n",
              "0   Mental illnesses are health conditions that di...          0.199049\n",
              "4   We encourage those with symptoms to talk to th...          0.143517"
            ]
          },
          "execution_count": 30,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "threshold = 0.1                                                                                   # considering the value of smiliarity to be greater than 0.1\n",
        "df_threshold = df_simi_tfidf_sort[df_simi_tfidf_sort['similarity_tfidf'] > threshold] \n",
        "df_threshold"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 31,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Un2v35qzCn6X",
        "outputId": "6eb29949-231c-4e17-e58d-3c5b118ae540"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "6"
            ]
          },
          "execution_count": 31,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "index_value1 = cos.argmax()                                                   # returns the index number of highest value\n",
        "index_value1"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 32,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "id": "4C0KLnatCuH9",
        "outputId": "2f342730-6261-47ea-d7f0-4784b9291107"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "'Different treatment options are available for individuals with mental illness.'"
            ]
          },
          "execution_count": 32,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df['Answers'].loc[index_value1]                                               # returns the text at that index"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "IhDZhgV5WI7g"
      },
      "source": [
        "# Testing chatbot"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 33,
      "metadata": {
        "id": "ri3aOkDVC34P"
      },
      "outputs": [],
      "source": [
        "# defining a function that returns response to query using bow\n",
        "\n",
        "def chat_bow(text):\n",
        "    lemma = text_normalization(text) # calling the function to perform text normalization\n",
        "    bow = cv.transform([lemma]).toarray() # applying bow\n",
        "    cosine_value = 1- pairwise_distances(df_bow,bow, metric = 'cosine' )\n",
        "    index_value = cosine_value.argmax() # getting index value \n",
        "    return df['Answers'].loc[index_value]"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 34,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "id": "kfGihw_jC8Fz",
        "outputId": "6107a3f9-a491-4bf7-ba51-fdc907324f4c"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "'When healing from mental illness, early identification and treatment are of vital importance. '"
            ]
          },
          "execution_count": 34,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "chat_bow('can you prevent mental health problems')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 35,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "id": "5p5rATqPDl1o",
        "outputId": "5978404a-c27f-4277-f70c-89e879dab764"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "'Different treatment options are available for individuals with mental illness.'"
            ]
          },
          "execution_count": 35,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "chat_bow('what is mental health')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 36,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "id": "j2pjkWnvD5d5",
        "outputId": "25bf5afe-13d4-42f2-d758-a0fe34a2d6d8"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "'Different treatment options are available for individuals with mental illness.'"
            ]
          },
          "execution_count": 36,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "chat_bow('are there cures for mental health problems')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 37,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "id": "mdnxBzdgDrFw",
        "outputId": "13991a7f-4890-4113-bf0c-39b3104396b4"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "'Create a plan for switching to a different treatment that will be a better fit.'"
            ]
          },
          "execution_count": 37,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "chat_bow('how do I know if i am unwell')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 38,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "id": "JHv1q2t_EETl",
        "outputId": "80cccda1-d2b7-4b73-9bee-26ebda4014e9"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "\"Mental illnesses are health conditions that disrupt a person's thoughts, emotions, relationships, and daily functioning.\""
            ]
          },
          "execution_count": 38,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "chat_bow('what do you mean by mental health')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 39,
      "metadata": {
        "id": "kWCumn0vELvd"
      },
      "outputs": [],
      "source": [
        "# defining a function that returns response to query using tf-idf\n",
        "\n",
        "def chat_tfidf(text):\n",
        "    lemma = text_normalization(text) # calling the function to perform text normalization\n",
        "    tf = tfidf.transform([lemma]).toarray() # applying tf-idf\n",
        "    cos = 1-pairwise_distances(df_tfidf,tf,metric='cosine') # applying cosine similarity\n",
        "    index_value = cos.argmax() # getting index value \n",
        "    return df['Answers'].loc[index_value]"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 40,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "id": "TLcTyog2Ea2t",
        "outputId": "74eff99b-6e9d-44f3-93a4-15aada6320ad"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "'Visit Healthfinder.gov to learn more.'"
            ]
          },
          "execution_count": 40,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "chat_tfidf('how do i see a counsellor')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 41,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "id": "YBK2XUM-Ek29",
        "outputId": "144fa0a1-96b7-4967-daf0-3a95a0bbe9a6"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "'Visit Healthfinder.gov to learn more.'"
            ]
          },
          "execution_count": 41,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "chat_tfidf('how to find a support group')"
      ]
    }
  ],
  "metadata": {
    "colab": {
      "collapsed_sections": [],
      "name": "Rule based",
      "provenance": [],
      "toc_visible": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8.18"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}