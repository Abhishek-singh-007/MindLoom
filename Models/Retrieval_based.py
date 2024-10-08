{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "K5y_I0O-5RMh"
      },
      "source": [
        "## Loading data and preliminary analysis"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {},
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Note: you may need to restart the kernel to use updated packages.\n"
          ]
        },
        {
          "data": {
            "text/plain": [
              "True"
            ]
          },
          "execution_count": 1,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "# Download Dependencies\n",
        "\n",
        "%pip install -r '../requirements.txt'\n",
        "\n",
        "import nltk \n",
        "\n",
        "nltk.download('stopwords')\n",
        "nltk.download('wordnet')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "id": "YR-ilUaKO1mR"
      },
      "outputs": [],
      "source": [
        "# import libraries\n",
        "\n",
        "import pandas as pd \n",
        "import numpy as np \n",
        "import matplotlib.pyplot as plt\n",
        "from pathlib import Path\n",
        "import string\n",
        "import re\n",
        "import joblib\n",
        "import json\n",
        "from collections import Counter\n",
        "from nltk.corpus import stopwords\n",
        "from nltk.stem import WordNetLemmatizer\n",
        "import pickle\n",
        "import tensorflow as tf\n",
        "from sklearn.preprocessing import LabelEncoder\n",
        "import os\n",
        "\n",
        "from tensorflow.keras.models import load_model\n",
        "from tensorflow.keras.preprocessing.text import Tokenizer\n",
        "from tensorflow.keras.preprocessing.sequence import pad_sequences\n",
        "from tensorflow.keras.utils import plot_model\n",
        "from tensorflow.keras.models import Sequential, Model\n",
        "from tensorflow.keras.layers import Embedding, Dense, Flatten, Conv1D, MaxPooling1D, SimpleRNN, GRU, LSTM, LSTM, Input, Embedding, TimeDistributed, Flatten, Dropout,Bidirectional\n",
        "from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 3,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Modify Paths\n",
        "\n",
        "path_to_json = '../Dataset/mentalhealth.json'\n",
        "path_to_dumps = '../Dumps/'\n",
        "\n",
        "newpath = path_to_dumps\n",
        "if not os.path.exists(newpath):\n",
        "    os.makedirs(newpath)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 4,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "EnLqRE6uS2Hb",
        "outputId": "470b6d1a-7f26-4d8e-b60c-48e3db2e2991"
      },
      "outputs": [],
      "source": [
        "# load data\n",
        "with open(path_to_json) as file:\n",
        "  data = json.load(file)\n",
        "\n",
        "# data"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 5,
      "metadata": {
        "id": "UHalec2-OgjC"
      },
      "outputs": [],
      "source": [
        "# convert to dataframes \n",
        " \n",
        "def frame_data(feat_1,feat_2,is_pattern, data):\n",
        "  is_pattern = is_pattern\n",
        "  df = pd.DataFrame(columns=[feat_1,feat_2])\n",
        "\n",
        "  for intent in data['intents']:\n",
        "    if is_pattern:\n",
        "      for pattern in intent['patterns']:\n",
        "        w = pattern\n",
        "        data_to_append = {feat_1:w, feat_2:intent['tag']}\n",
        "        df.loc[len(df)] = data_to_append\n",
        "        \n",
        "    else:\n",
        "      for response in intent['responses']:\n",
        "        w = response\n",
        "        data_to_append = {feat_1:w, feat_2:intent['tag']}\n",
        "        df.loc[len(df)] = data_to_append\n",
        "  return df"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 6,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 203
        },
        "id": "nzHe4LRwS7KL",
        "outputId": "ef19fb8a-89f4-42ea-e294-e32758e746ea"
      },
      "outputs": [],
      "source": [
        "df1 = frame_data('questions','labels',True, data)\n",
        "# df1.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 7,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "dBK6Wzi-S7GW",
        "outputId": "861808e1-063b-4d1f-b0d7-dd5564e2ee30"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "labels\n",
              "definition            3\n",
              "affects_whom          2\n",
              "what_causes           3\n",
              "recover               2\n",
              "steps                 2\n",
              "find_help             2\n",
              "treatement_options    2\n",
              "treatment_tips        2\n",
              "professional_types    2\n",
              "right_professional    2\n",
              "Name: count, dtype: int64"
            ]
          },
          "execution_count": 7,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "# no of patterns\n",
        "\n",
        "df1.labels.value_counts(sort=False)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 8,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 203
        },
        "id": "me9oCoFmS7EI",
        "outputId": "730658df-9755-4b6f-fba7-68904e0f1ae0"
      },
      "outputs": [],
      "source": [
        "df2 = frame_data('response','labels',False, data)\n",
        "# df2.head()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Ja0_TgzN5Xya"
      },
      "source": [
        "## Data preprocessing"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 9,
      "metadata": {
        "id": "YEVlJqEIR_ts"
      },
      "outputs": [],
      "source": [
        "# preprocessing text\n",
        "\n",
        "lemmatizer = WordNetLemmatizer()\n",
        "\n",
        "vocab = Counter()\n",
        "labels = []\n",
        "def tokenizer(entry):\n",
        "    tokens = entry.split()\n",
        "    re_punc = re.compile('[%s]' % re.escape(string.punctuation))\n",
        "    tokens = [re_punc.sub('', w) for w in tokens]\n",
        "    tokens = [word for word in tokens if word.isalpha()]\n",
        "    tokens = [lemmatizer.lemmatize(w.lower()) for w in tokens]\n",
        "    tokens = [word.lower() for word in tokens if len(word) > 1]\n",
        "    return tokens\n",
        "\n",
        "def remove_stop_words(tokenizer,df,feature):\n",
        "    doc_without_stopwords = []\n",
        "    for entry in df[feature]:\n",
        "        tokens = tokenizer(entry)\n",
        "        joblib.dump(tokens,path_to_dumps+'tokens.pkl')\n",
        "        doc_without_stopwords.append(' '.join(tokens))\n",
        "    df[feature] = doc_without_stopwords\n",
        "    return"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 10,
      "metadata": {
        "id": "Jt61ZCG9UWN0"
      },
      "outputs": [],
      "source": [
        "def create_vocab(tokenizer,df,feature):\n",
        "    for entry in df[feature]:\n",
        "        tokens = tokenizer(entry)   \n",
        "        vocab.update(tokens)\n",
        "    joblib.dump(vocab, path_to_dumps+'vocab.pkl')\n",
        "    return"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 11,
      "metadata": {
        "id": "emdwHIQcUWJ-"
      },
      "outputs": [],
      "source": [
        "create_vocab(tokenizer,df1,'questions')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 12,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "IbK9OeYY0iWo",
        "outputId": "e058ceab-cdd4-4b40-eb08-ad9246b607d3"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "Counter({'what': 9,\n",
              "         'doe': 3,\n",
              "         'it': 2,\n",
              "         'mean': 1,\n",
              "         'to': 9,\n",
              "         'have': 2,\n",
              "         'mental': 14,\n",
              "         'illness': 9,\n",
              "         'is': 4,\n",
              "         'health': 8,\n",
              "         'describe': 1,\n",
              "         'who': 3,\n",
              "         'affect': 1,\n",
              "         'affected': 1,\n",
              "         'by': 1,\n",
              "         'mentall': 1,\n",
              "         'cause': 1,\n",
              "         'lead': 1,\n",
              "         'how': 7,\n",
              "         'one': 2,\n",
              "         'get': 1,\n",
              "         'mentally': 1,\n",
              "         'ill': 1,\n",
              "         'can': 3,\n",
              "         'people': 1,\n",
              "         'with': 1,\n",
              "         'recover': 3,\n",
              "         'possible': 1,\n",
              "         'from': 1,\n",
              "         'know': 1,\n",
              "         'someone': 1,\n",
              "         'appears': 1,\n",
              "         'such': 1,\n",
              "         'symptom': 2,\n",
              "         'are': 3,\n",
              "         'the': 4,\n",
              "         'step': 1,\n",
              "         'be': 1,\n",
              "         'followed': 1,\n",
              "         'incase': 1,\n",
              "         'of': 2,\n",
              "         'find': 4,\n",
              "         'professional': 6,\n",
              "         'for': 1,\n",
              "         'myself': 2,\n",
              "         'treatment': 3,\n",
              "         'option': 1,\n",
              "         'available': 1,\n",
              "         'become': 1,\n",
              "         'involved': 1,\n",
              "         'in': 2,\n",
              "         'should': 1,\n",
              "         'keep': 1,\n",
              "         'mind': 1,\n",
              "         'if': 1,\n",
              "         'begin': 1,\n",
              "         'difference': 1,\n",
              "         'between': 1,\n",
              "         'different': 1,\n",
              "         'type': 1,\n",
              "         'present': 1,\n",
              "         'right': 2})"
            ]
          },
          "execution_count": 12,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "vocab"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 13,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "0_EER8ZWkpJU",
        "outputId": "0b272597-4ea5-44dd-f37a-2c7df0e8731a"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "62"
            ]
          },
          "execution_count": 13,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "vocab_size = len(vocab)\n",
        "vocab_size"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 14,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "q2S6fc7iV5Fl",
        "outputId": "23324a36-3505-45b6-a5cc-2e48ac3da410"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "0                      Who does mental illness affect?\n",
              "1          What does it mean to have a mental illness?\n",
              "2    How to find mental health professional for myself\n",
              "3    What is the difference between mental health p...\n",
              "4              Can people with mental illness recover?\n",
              "5    How can I find a mental health professional ri...\n",
              "6    I know someone who appears to have such symptoms?\n",
              "7                What treatment options are available?\n",
              "8                 How to become involved in treatment?\n",
              "9                          What causes mental illness?\n",
              "Name: questions, dtype: object"
            ]
          },
          "execution_count": 14,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df1.groupby(by='labels',as_index=False).first()['questions']"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 15,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "flmw4NGyR_o1",
        "outputId": "63f1c0f6-4587-4093-ed72-f3213e5449e4"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "['Who does mental illness affect?',\n",
              " 'What does it mean to have a mental illness?',\n",
              " 'How to find mental health professional for myself',\n",
              " 'What is the difference between mental health professionals?',\n",
              " 'Can people with mental illness recover?',\n",
              " 'How can I find a mental health professional right myself?',\n",
              " 'I know someone who appears to have such symptoms?',\n",
              " 'What treatment options are available?',\n",
              " 'How to become involved in treatment?',\n",
              " 'What causes mental illness?']"
            ]
          },
          "execution_count": 15,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "# test_list contains the first element of questions\n",
        "\n",
        "test_list = list(df1.groupby(by='labels',as_index=False).first()['questions'])\n",
        "test_list"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 16,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "MNtMUqJQUs9U",
        "outputId": "033574e0-71f2-411b-8bc6-6ae9557fd3c5"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "[3, 0, 12, 18, 8, 20, 10, 14, 16, 5]"
            ]
          },
          "execution_count": 16,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "# indices of the testing dataset\n",
        "\n",
        "test_index = []\n",
        "for i,_ in enumerate(test_list):\n",
        "    idx = df1[df1.questions == test_list[i]].index[0]\n",
        "    test_index.append(idx)\n",
        "test_index"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 17,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Reko6L-LUs6e",
        "outputId": "30ace821-537d-4573-980b-787511baabf6"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "[1, 2, 4, 6, 7, 9, 11, 13, 15, 17, 19, 21]"
            ]
          },
          "execution_count": 17,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "# train indices are the all indices minus the testing indices \n",
        "\n",
        "train_index = [i for i in df1.index if i not in test_index]\n",
        "train_index "
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 18,
      "metadata": {
        "id": "u-ksA3SrUs3a"
      },
      "outputs": [],
      "source": [
        "def convert_seq(df,feature):\n",
        "#     text = ' '.join(list(vocab.keys()))\n",
        "    t = Tokenizer()\n",
        "    entries = [entry for entry in df[feature]]\n",
        "    print(entries)\n",
        "    print('----')\n",
        "    t.fit_on_texts(entries)\n",
        "    joblib.dump(t, path_to_dumps+'tokenizer_t.pkl')   # why a pkl file\n",
        "    vocab_size = len(t.word_index) +1 # +1 for oov \n",
        "    print(t.word_index)\n",
        "    entries = [entry for entry in df[feature]]\n",
        "    max_length = max([len(s.split()) for s in entries])\n",
        "    print('----')\n",
        "    print(\"max length of string is : \",max_length)\n",
        "    print('----')\n",
        "    encoded = t.texts_to_sequences(entries)\n",
        "    print(encoded)\n",
        "    padded = pad_sequences(encoded, maxlen=max_length, padding='post')\n",
        "    print('----')\n",
        "    print(padded)\n",
        "    return padded, vocab_size"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "VjFFIlul53UZ"
      },
      "source": [
        "**fit_on_texts** updates internal vocabulary based on a list of texts. This method creates the vocabulary index based on word frequency. 0 is reserved for padding. So lower integer means more frequent word (often the first few are stop words because they appear a lot)."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "z5a_RLov7R2s"
      },
      "source": [
        "Now that we have a vocabulary of words in the dataset, **each of the patterns can be encoded into numerical features for modeling, using any of the common text encoding techniques—count vectorizer**, term frequency-inverse document frequency (TF-IDF), hashing, etc.\n",
        "\n",
        "Using TensorFlow.Keras text_to_sequence, we can **encode each pattern corpus to vectorize a text corpus by turning each text into either a sequence of integers** (each integer being the index of a token in a dictionary) or into a vector where the coefficient for each token could be binary, based on word count which is based on TF-IDF. The resulting vectors will be post-padded with zeros so as to equal the length of the vectors."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 19,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "GP07TFsDUs0e",
        "outputId": "7c2ace6d-31ad-464f-edb9-e0e606ad1f82"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "['What does it mean to have a mental illness?', 'What is mental health illness', 'Describe mental health illness', 'Who does mental illness affect?', 'Who is affected by mentall illness', 'What causes mental illness?', 'What leads to mental illness?', 'how does one get mentally ill?', 'Can people with mental illness recover?', 'Is it possible to recover from mental illness', 'I know someone who appears to have such symptoms?', 'What are the steps to be followed incase of symptoms', 'How to find mental health professional for myself', 'How to find mental health professional?', 'What treatment options are available?', 'How can one recover?', 'How to become involved in treatment?', 'What should I keep in mind if I begin treatment?', 'What is the difference between mental health professionals?', 'What are the different types of mental health professionals present?', 'How can I find a mental health professional right myself?', 'How to find the right mental health professional?']\n",
            "----\n",
            "{'mental': 1, 'what': 2, 'to': 3, 'illness': 4, 'health': 5, 'how': 6, 'is': 7, 'i': 8, 'the': 9, 'find': 10, 'professional': 11, 'does': 12, 'who': 13, 'can': 14, 'recover': 15, 'are': 16, 'treatment': 17, 'it': 18, 'have': 19, 'a': 20, 'one': 21, 'symptoms': 22, 'of': 23, 'myself': 24, 'in': 25, 'professionals': 26, 'right': 27, 'mean': 28, 'describe': 29, 'affect': 30, 'affected': 31, 'by': 32, 'mentall': 33, 'causes': 34, 'leads': 35, 'get': 36, 'mentally': 37, 'ill': 38, 'people': 39, 'with': 40, 'possible': 41, 'from': 42, 'know': 43, 'someone': 44, 'appears': 45, 'such': 46, 'steps': 47, 'be': 48, 'followed': 49, 'incase': 50, 'for': 51, 'options': 52, 'available': 53, 'become': 54, 'involved': 55, 'should': 56, 'keep': 57, 'mind': 58, 'if': 59, 'begin': 60, 'difference': 61, 'between': 62, 'different': 63, 'types': 64, 'present': 65}\n",
            "----\n",
            "max length of string is :  10\n",
            "----\n",
            "[[2, 12, 18, 28, 3, 19, 20, 1, 4], [2, 7, 1, 5, 4], [29, 1, 5, 4], [13, 12, 1, 4, 30], [13, 7, 31, 32, 33, 4], [2, 34, 1, 4], [2, 35, 3, 1, 4], [6, 12, 21, 36, 37, 38], [14, 39, 40, 1, 4, 15], [7, 18, 41, 3, 15, 42, 1, 4], [8, 43, 44, 13, 45, 3, 19, 46, 22], [2, 16, 9, 47, 3, 48, 49, 50, 23, 22], [6, 3, 10, 1, 5, 11, 51, 24], [6, 3, 10, 1, 5, 11], [2, 17, 52, 16, 53], [6, 14, 21, 15], [6, 3, 54, 55, 25, 17], [2, 56, 8, 57, 25, 58, 59, 8, 60, 17], [2, 7, 9, 61, 62, 1, 5, 26], [2, 16, 9, 63, 64, 23, 1, 5, 26, 65], [6, 14, 8, 10, 20, 1, 5, 11, 27, 24], [6, 3, 10, 9, 27, 1, 5, 11]]\n",
            "----\n",
            "[[ 2 12 18 28  3 19 20  1  4  0]\n",
            " [ 2  7  1  5  4  0  0  0  0  0]\n",
            " [29  1  5  4  0  0  0  0  0  0]\n",
            " [13 12  1  4 30  0  0  0  0  0]\n",
            " [13  7 31 32 33  4  0  0  0  0]\n",
            " [ 2 34  1  4  0  0  0  0  0  0]\n",
            " [ 2 35  3  1  4  0  0  0  0  0]\n",
            " [ 6 12 21 36 37 38  0  0  0  0]\n",
            " [14 39 40  1  4 15  0  0  0  0]\n",
            " [ 7 18 41  3 15 42  1  4  0  0]\n",
            " [ 8 43 44 13 45  3 19 46 22  0]\n",
            " [ 2 16  9 47  3 48 49 50 23 22]\n",
            " [ 6  3 10  1  5 11 51 24  0  0]\n",
            " [ 6  3 10  1  5 11  0  0  0  0]\n",
            " [ 2 17 52 16 53  0  0  0  0  0]\n",
            " [ 6 14 21 15  0  0  0  0  0  0]\n",
            " [ 6  3 54 55 25 17  0  0  0  0]\n",
            " [ 2 56  8 57 25 58 59  8 60 17]\n",
            " [ 2  7  9 61 62  1  5 26  0  0]\n",
            " [ 2 16  9 63 64 23  1  5 26 65]\n",
            " [ 6 14  8 10 20  1  5 11 27 24]\n",
            " [ 6  3 10  9 27  1  5 11  0  0]]\n"
          ]
        }
      ],
      "source": [
        "X,vocab_size = convert_seq(df1,'questions')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 20,
      "metadata": {
        "id": "TjqSgtug5uSU"
      },
      "outputs": [],
      "source": [
        "with open(path_to_dumps+'tokenizer_t.pkl', 'rb') as f:\n",
        "    data = pickle.load(f)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 21,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Ww0VWLGV6WDo",
        "outputId": "590e3660-78a5-4e56-fac3-3585f7a55cae"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "{1: 'mental',\n",
              " 2: 'what',\n",
              " 3: 'to',\n",
              " 4: 'illness',\n",
              " 5: 'health',\n",
              " 6: 'how',\n",
              " 7: 'is',\n",
              " 8: 'i',\n",
              " 9: 'the',\n",
              " 10: 'find',\n",
              " 11: 'professional',\n",
              " 12: 'does',\n",
              " 13: 'who',\n",
              " 14: 'can',\n",
              " 15: 'recover',\n",
              " 16: 'are',\n",
              " 17: 'treatment',\n",
              " 18: 'it',\n",
              " 19: 'have',\n",
              " 20: 'a',\n",
              " 21: 'one',\n",
              " 22: 'symptoms',\n",
              " 23: 'of',\n",
              " 24: 'myself',\n",
              " 25: 'in',\n",
              " 26: 'professionals',\n",
              " 27: 'right',\n",
              " 28: 'mean',\n",
              " 29: 'describe',\n",
              " 30: 'affect',\n",
              " 31: 'affected',\n",
              " 32: 'by',\n",
              " 33: 'mentall',\n",
              " 34: 'causes',\n",
              " 35: 'leads',\n",
              " 36: 'get',\n",
              " 37: 'mentally',\n",
              " 38: 'ill',\n",
              " 39: 'people',\n",
              " 40: 'with',\n",
              " 41: 'possible',\n",
              " 42: 'from',\n",
              " 43: 'know',\n",
              " 44: 'someone',\n",
              " 45: 'appears',\n",
              " 46: 'such',\n",
              " 47: 'steps',\n",
              " 48: 'be',\n",
              " 49: 'followed',\n",
              " 50: 'incase',\n",
              " 51: 'for',\n",
              " 52: 'options',\n",
              " 53: 'available',\n",
              " 54: 'become',\n",
              " 55: 'involved',\n",
              " 56: 'should',\n",
              " 57: 'keep',\n",
              " 58: 'mind',\n",
              " 59: 'if',\n",
              " 60: 'begin',\n",
              " 61: 'difference',\n",
              " 62: 'between',\n",
              " 63: 'different',\n",
              " 64: 'types',\n",
              " 65: 'present'}"
            ]
          },
          "execution_count": 21,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "data.index_word"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 22,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "4TKUtsd851W4",
        "outputId": "a5e422af-11a5-4bdb-ddfc-f0784fa84e4f"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "OrderedDict([('what', 9),\n",
              "             ('does', 3),\n",
              "             ('it', 2),\n",
              "             ('mean', 1),\n",
              "             ('to', 9),\n",
              "             ('have', 2),\n",
              "             ('a', 2),\n",
              "             ('mental', 14),\n",
              "             ('illness', 9),\n",
              "             ('is', 4),\n",
              "             ('health', 8),\n",
              "             ('describe', 1),\n",
              "             ('who', 3),\n",
              "             ('affect', 1),\n",
              "             ('affected', 1),\n",
              "             ('by', 1),\n",
              "             ('mentall', 1),\n",
              "             ('causes', 1),\n",
              "             ('leads', 1),\n",
              "             ('how', 7),\n",
              "             ('one', 2),\n",
              "             ('get', 1),\n",
              "             ('mentally', 1),\n",
              "             ('ill', 1),\n",
              "             ('can', 3),\n",
              "             ('people', 1),\n",
              "             ('with', 1),\n",
              "             ('recover', 3),\n",
              "             ('possible', 1),\n",
              "             ('from', 1),\n",
              "             ('i', 4),\n",
              "             ('know', 1),\n",
              "             ('someone', 1),\n",
              "             ('appears', 1),\n",
              "             ('such', 1),\n",
              "             ('symptoms', 2),\n",
              "             ('are', 3),\n",
              "             ('the', 4),\n",
              "             ('steps', 1),\n",
              "             ('be', 1),\n",
              "             ('followed', 1),\n",
              "             ('incase', 1),\n",
              "             ('of', 2),\n",
              "             ('find', 4),\n",
              "             ('professional', 4),\n",
              "             ('for', 1),\n",
              "             ('myself', 2),\n",
              "             ('treatment', 3),\n",
              "             ('options', 1),\n",
              "             ('available', 1),\n",
              "             ('become', 1),\n",
              "             ('involved', 1),\n",
              "             ('in', 2),\n",
              "             ('should', 1),\n",
              "             ('keep', 1),\n",
              "             ('mind', 1),\n",
              "             ('if', 1),\n",
              "             ('begin', 1),\n",
              "             ('difference', 1),\n",
              "             ('between', 1),\n",
              "             ('professionals', 2),\n",
              "             ('different', 1),\n",
              "             ('types', 1),\n",
              "             ('present', 1),\n",
              "             ('right', 2)])"
            ]
          },
          "execution_count": 22,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "data.word_counts"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 23,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "gExivERw6WdD",
        "outputId": "9f90dcea-abdc-4aff-cd32-e27616f2ddbe"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "array([[ 2, 12, 18, 28,  3, 19, 20,  1,  4,  0],\n",
              "       [ 2,  7,  1,  5,  4,  0,  0,  0,  0,  0],\n",
              "       [29,  1,  5,  4,  0,  0,  0,  0,  0,  0],\n",
              "       [13, 12,  1,  4, 30,  0,  0,  0,  0,  0],\n",
              "       [13,  7, 31, 32, 33,  4,  0,  0,  0,  0],\n",
              "       [ 2, 34,  1,  4,  0,  0,  0,  0,  0,  0],\n",
              "       [ 2, 35,  3,  1,  4,  0,  0,  0,  0,  0],\n",
              "       [ 6, 12, 21, 36, 37, 38,  0,  0,  0,  0],\n",
              "       [14, 39, 40,  1,  4, 15,  0,  0,  0,  0],\n",
              "       [ 7, 18, 41,  3, 15, 42,  1,  4,  0,  0],\n",
              "       [ 8, 43, 44, 13, 45,  3, 19, 46, 22,  0],\n",
              "       [ 2, 16,  9, 47,  3, 48, 49, 50, 23, 22],\n",
              "       [ 6,  3, 10,  1,  5, 11, 51, 24,  0,  0],\n",
              "       [ 6,  3, 10,  1,  5, 11,  0,  0,  0,  0],\n",
              "       [ 2, 17, 52, 16, 53,  0,  0,  0,  0,  0],\n",
              "       [ 6, 14, 21, 15,  0,  0,  0,  0,  0,  0],\n",
              "       [ 6,  3, 54, 55, 25, 17,  0,  0,  0,  0],\n",
              "       [ 2, 56,  8, 57, 25, 58, 59,  8, 60, 17],\n",
              "       [ 2,  7,  9, 61, 62,  1,  5, 26,  0,  0],\n",
              "       [ 2, 16,  9, 63, 64, 23,  1,  5, 26, 65],\n",
              "       [ 6, 14,  8, 10, 20,  1,  5, 11, 27, 24],\n",
              "       [ 6,  3, 10,  9, 27,  1,  5, 11,  0,  0]], dtype=int32)"
            ]
          },
          "execution_count": 23,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "X"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 24,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "bimUOhFb6Y_9",
        "outputId": "91159b95-22dd-4f6f-a8bd-17d10ebf9c0f"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "66"
            ]
          },
          "execution_count": 24,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "vocab_size"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 25,
      "metadata": {
        "id": "4cKWHDabXLg_"
      },
      "outputs": [],
      "source": [
        "df_encoded = pd.DataFrame(X)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 26,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 726
        },
        "id": "wfjo-4088OnX",
        "outputId": "d6f6a60e-7f8e-40f5-ca50-69062a34d4fa"
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
              "      <th>0</th>\n",
              "      <th>1</th>\n",
              "      <th>2</th>\n",
              "      <th>3</th>\n",
              "      <th>4</th>\n",
              "      <th>5</th>\n",
              "      <th>6</th>\n",
              "      <th>7</th>\n",
              "      <th>8</th>\n",
              "      <th>9</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>2</td>\n",
              "      <td>12</td>\n",
              "      <td>18</td>\n",
              "      <td>28</td>\n",
              "      <td>3</td>\n",
              "      <td>19</td>\n",
              "      <td>20</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>2</td>\n",
              "      <td>7</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>29</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>13</td>\n",
              "      <td>12</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>30</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>13</td>\n",
              "      <td>7</td>\n",
              "      <td>31</td>\n",
              "      <td>32</td>\n",
              "      <td>33</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>2</td>\n",
              "      <td>34</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>2</td>\n",
              "      <td>35</td>\n",
              "      <td>3</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>6</td>\n",
              "      <td>12</td>\n",
              "      <td>21</td>\n",
              "      <td>36</td>\n",
              "      <td>37</td>\n",
              "      <td>38</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>14</td>\n",
              "      <td>39</td>\n",
              "      <td>40</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>15</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>7</td>\n",
              "      <td>18</td>\n",
              "      <td>41</td>\n",
              "      <td>3</td>\n",
              "      <td>15</td>\n",
              "      <td>42</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>10</th>\n",
              "      <td>8</td>\n",
              "      <td>43</td>\n",
              "      <td>44</td>\n",
              "      <td>13</td>\n",
              "      <td>45</td>\n",
              "      <td>3</td>\n",
              "      <td>19</td>\n",
              "      <td>46</td>\n",
              "      <td>22</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>11</th>\n",
              "      <td>2</td>\n",
              "      <td>16</td>\n",
              "      <td>9</td>\n",
              "      <td>47</td>\n",
              "      <td>3</td>\n",
              "      <td>48</td>\n",
              "      <td>49</td>\n",
              "      <td>50</td>\n",
              "      <td>23</td>\n",
              "      <td>22</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>12</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>51</td>\n",
              "      <td>24</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>14</th>\n",
              "      <td>2</td>\n",
              "      <td>17</td>\n",
              "      <td>52</td>\n",
              "      <td>16</td>\n",
              "      <td>53</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>15</th>\n",
              "      <td>6</td>\n",
              "      <td>14</td>\n",
              "      <td>21</td>\n",
              "      <td>15</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>16</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>54</td>\n",
              "      <td>55</td>\n",
              "      <td>25</td>\n",
              "      <td>17</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>17</th>\n",
              "      <td>2</td>\n",
              "      <td>56</td>\n",
              "      <td>8</td>\n",
              "      <td>57</td>\n",
              "      <td>25</td>\n",
              "      <td>58</td>\n",
              "      <td>59</td>\n",
              "      <td>8</td>\n",
              "      <td>60</td>\n",
              "      <td>17</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>18</th>\n",
              "      <td>2</td>\n",
              "      <td>7</td>\n",
              "      <td>9</td>\n",
              "      <td>61</td>\n",
              "      <td>62</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>26</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>19</th>\n",
              "      <td>2</td>\n",
              "      <td>16</td>\n",
              "      <td>9</td>\n",
              "      <td>63</td>\n",
              "      <td>64</td>\n",
              "      <td>23</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>26</td>\n",
              "      <td>65</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>20</th>\n",
              "      <td>6</td>\n",
              "      <td>14</td>\n",
              "      <td>8</td>\n",
              "      <td>10</td>\n",
              "      <td>20</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>27</td>\n",
              "      <td>24</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>21</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>9</td>\n",
              "      <td>27</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "     0   1   2   3   4   5   6   7   8   9\n",
              "0    2  12  18  28   3  19  20   1   4   0\n",
              "1    2   7   1   5   4   0   0   0   0   0\n",
              "2   29   1   5   4   0   0   0   0   0   0\n",
              "3   13  12   1   4  30   0   0   0   0   0\n",
              "4   13   7  31  32  33   4   0   0   0   0\n",
              "5    2  34   1   4   0   0   0   0   0   0\n",
              "6    2  35   3   1   4   0   0   0   0   0\n",
              "7    6  12  21  36  37  38   0   0   0   0\n",
              "8   14  39  40   1   4  15   0   0   0   0\n",
              "9    7  18  41   3  15  42   1   4   0   0\n",
              "10   8  43  44  13  45   3  19  46  22   0\n",
              "11   2  16   9  47   3  48  49  50  23  22\n",
              "12   6   3  10   1   5  11  51  24   0   0\n",
              "13   6   3  10   1   5  11   0   0   0   0\n",
              "14   2  17  52  16  53   0   0   0   0   0\n",
              "15   6  14  21  15   0   0   0   0   0   0\n",
              "16   6   3  54  55  25  17   0   0   0   0\n",
              "17   2  56   8  57  25  58  59   8  60  17\n",
              "18   2   7   9  61  62   1   5  26   0   0\n",
              "19   2  16   9  63  64  23   1   5  26  65\n",
              "20   6  14   8  10  20   1   5  11  27  24\n",
              "21   6   3  10   9  27   1   5  11   0   0"
            ]
          },
          "execution_count": 26,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df_encoded"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 27,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 357
        },
        "id": "Dje2hCaJ8IPc",
        "outputId": "3a3d5190-13bc-4118-f953-07d0ed5dd3de"
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
              "      <th>questions</th>\n",
              "      <th>labels</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>What does it mean to have a mental illness?</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>What is mental health illness</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Describe mental health illness</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>Who does mental illness affect?</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>Who is affected by mentall illness</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>What causes mental illness?</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>What leads to mental illness?</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>how does one get mentally ill?</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>Can people with mental illness recover?</td>\n",
              "      <td>recover</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>Is it possible to recover from mental illness</td>\n",
              "      <td>recover</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "                                       questions        labels\n",
              "0    What does it mean to have a mental illness?    definition\n",
              "1                  What is mental health illness    definition\n",
              "2                 Describe mental health illness    definition\n",
              "3                Who does mental illness affect?  affects_whom\n",
              "4             Who is affected by mentall illness  affects_whom\n",
              "5                    What causes mental illness?   what_causes\n",
              "6                  What leads to mental illness?   what_causes\n",
              "7                 how does one get mentally ill?   what_causes\n",
              "8        Can people with mental illness recover?       recover\n",
              "9  Is it possible to recover from mental illness       recover"
            ]
          },
          "execution_count": 27,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df1.head(10)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 28,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 357
        },
        "id": "3Uu_JiN5XLdt",
        "outputId": "d83accbd-8cfe-4b46-9cc4-6b39a218172f"
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
              "      <th>0</th>\n",
              "      <th>1</th>\n",
              "      <th>2</th>\n",
              "      <th>3</th>\n",
              "      <th>4</th>\n",
              "      <th>5</th>\n",
              "      <th>6</th>\n",
              "      <th>7</th>\n",
              "      <th>8</th>\n",
              "      <th>9</th>\n",
              "      <th>labels</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>2</td>\n",
              "      <td>12</td>\n",
              "      <td>18</td>\n",
              "      <td>28</td>\n",
              "      <td>3</td>\n",
              "      <td>19</td>\n",
              "      <td>20</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>2</td>\n",
              "      <td>7</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>29</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>13</td>\n",
              "      <td>12</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>30</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>13</td>\n",
              "      <td>7</td>\n",
              "      <td>31</td>\n",
              "      <td>32</td>\n",
              "      <td>33</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>2</td>\n",
              "      <td>34</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>2</td>\n",
              "      <td>35</td>\n",
              "      <td>3</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>6</td>\n",
              "      <td>12</td>\n",
              "      <td>21</td>\n",
              "      <td>36</td>\n",
              "      <td>37</td>\n",
              "      <td>38</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>14</td>\n",
              "      <td>39</td>\n",
              "      <td>40</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>15</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>recover</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>7</td>\n",
              "      <td>18</td>\n",
              "      <td>41</td>\n",
              "      <td>3</td>\n",
              "      <td>15</td>\n",
              "      <td>42</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>recover</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "    0   1   2   3   4   5   6  7  8  9        labels\n",
              "0   2  12  18  28   3  19  20  1  4  0    definition\n",
              "1   2   7   1   5   4   0   0  0  0  0    definition\n",
              "2  29   1   5   4   0   0   0  0  0  0    definition\n",
              "3  13  12   1   4  30   0   0  0  0  0  affects_whom\n",
              "4  13   7  31  32  33   4   0  0  0  0  affects_whom\n",
              "5   2  34   1   4   0   0   0  0  0  0   what_causes\n",
              "6   2  35   3   1   4   0   0  0  0  0   what_causes\n",
              "7   6  12  21  36  37  38   0  0  0  0   what_causes\n",
              "8  14  39  40   1   4  15   0  0  0  0       recover\n",
              "9   7  18  41   3  15  42   1  4  0  0       recover"
            ]
          },
          "execution_count": 28,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df_encoded['labels'] = df1.labels\n",
        "df_encoded.head(10)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 29,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 726
        },
        "id": "heGzmZM3XS4J",
        "outputId": "ed09e08b-e76f-48c2-da63-99e09df7e653"
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
              "      <th>0</th>\n",
              "      <th>1</th>\n",
              "      <th>2</th>\n",
              "      <th>3</th>\n",
              "      <th>4</th>\n",
              "      <th>5</th>\n",
              "      <th>6</th>\n",
              "      <th>7</th>\n",
              "      <th>8</th>\n",
              "      <th>9</th>\n",
              "      <th>labels</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>2</td>\n",
              "      <td>12</td>\n",
              "      <td>18</td>\n",
              "      <td>28</td>\n",
              "      <td>3</td>\n",
              "      <td>19</td>\n",
              "      <td>20</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>2</td>\n",
              "      <td>7</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>29</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>13</td>\n",
              "      <td>12</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>30</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>13</td>\n",
              "      <td>7</td>\n",
              "      <td>31</td>\n",
              "      <td>32</td>\n",
              "      <td>33</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>2</td>\n",
              "      <td>34</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>2</td>\n",
              "      <td>35</td>\n",
              "      <td>3</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>6</td>\n",
              "      <td>12</td>\n",
              "      <td>21</td>\n",
              "      <td>36</td>\n",
              "      <td>37</td>\n",
              "      <td>38</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>14</td>\n",
              "      <td>39</td>\n",
              "      <td>40</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>15</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>recover</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>7</td>\n",
              "      <td>18</td>\n",
              "      <td>41</td>\n",
              "      <td>3</td>\n",
              "      <td>15</td>\n",
              "      <td>42</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>recover</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>10</th>\n",
              "      <td>8</td>\n",
              "      <td>43</td>\n",
              "      <td>44</td>\n",
              "      <td>13</td>\n",
              "      <td>45</td>\n",
              "      <td>3</td>\n",
              "      <td>19</td>\n",
              "      <td>46</td>\n",
              "      <td>22</td>\n",
              "      <td>0</td>\n",
              "      <td>steps</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>11</th>\n",
              "      <td>2</td>\n",
              "      <td>16</td>\n",
              "      <td>9</td>\n",
              "      <td>47</td>\n",
              "      <td>3</td>\n",
              "      <td>48</td>\n",
              "      <td>49</td>\n",
              "      <td>50</td>\n",
              "      <td>23</td>\n",
              "      <td>22</td>\n",
              "      <td>steps</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>12</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>51</td>\n",
              "      <td>24</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>find_help</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>find_help</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>14</th>\n",
              "      <td>2</td>\n",
              "      <td>17</td>\n",
              "      <td>52</td>\n",
              "      <td>16</td>\n",
              "      <td>53</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>treatement_options</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>15</th>\n",
              "      <td>6</td>\n",
              "      <td>14</td>\n",
              "      <td>21</td>\n",
              "      <td>15</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>treatement_options</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>16</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>54</td>\n",
              "      <td>55</td>\n",
              "      <td>25</td>\n",
              "      <td>17</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>treatment_tips</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>17</th>\n",
              "      <td>2</td>\n",
              "      <td>56</td>\n",
              "      <td>8</td>\n",
              "      <td>57</td>\n",
              "      <td>25</td>\n",
              "      <td>58</td>\n",
              "      <td>59</td>\n",
              "      <td>8</td>\n",
              "      <td>60</td>\n",
              "      <td>17</td>\n",
              "      <td>treatment_tips</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>18</th>\n",
              "      <td>2</td>\n",
              "      <td>7</td>\n",
              "      <td>9</td>\n",
              "      <td>61</td>\n",
              "      <td>62</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>26</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>professional_types</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>19</th>\n",
              "      <td>2</td>\n",
              "      <td>16</td>\n",
              "      <td>9</td>\n",
              "      <td>63</td>\n",
              "      <td>64</td>\n",
              "      <td>23</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>26</td>\n",
              "      <td>65</td>\n",
              "      <td>professional_types</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>20</th>\n",
              "      <td>6</td>\n",
              "      <td>14</td>\n",
              "      <td>8</td>\n",
              "      <td>10</td>\n",
              "      <td>20</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>27</td>\n",
              "      <td>24</td>\n",
              "      <td>right_professional</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>21</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>9</td>\n",
              "      <td>27</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>right_professional</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "     0   1   2   3   4   5   6   7   8   9              labels\n",
              "0    2  12  18  28   3  19  20   1   4   0          definition\n",
              "1    2   7   1   5   4   0   0   0   0   0          definition\n",
              "2   29   1   5   4   0   0   0   0   0   0          definition\n",
              "3   13  12   1   4  30   0   0   0   0   0        affects_whom\n",
              "4   13   7  31  32  33   4   0   0   0   0        affects_whom\n",
              "5    2  34   1   4   0   0   0   0   0   0         what_causes\n",
              "6    2  35   3   1   4   0   0   0   0   0         what_causes\n",
              "7    6  12  21  36  37  38   0   0   0   0         what_causes\n",
              "8   14  39  40   1   4  15   0   0   0   0             recover\n",
              "9    7  18  41   3  15  42   1   4   0   0             recover\n",
              "10   8  43  44  13  45   3  19  46  22   0               steps\n",
              "11   2  16   9  47   3  48  49  50  23  22               steps\n",
              "12   6   3  10   1   5  11  51  24   0   0           find_help\n",
              "13   6   3  10   1   5  11   0   0   0   0           find_help\n",
              "14   2  17  52  16  53   0   0   0   0   0  treatement_options\n",
              "15   6  14  21  15   0   0   0   0   0   0  treatement_options\n",
              "16   6   3  54  55  25  17   0   0   0   0      treatment_tips\n",
              "17   2  56   8  57  25  58  59   8  60  17      treatment_tips\n",
              "18   2   7   9  61  62   1   5  26   0   0  professional_types\n",
              "19   2  16   9  63  64  23   1   5  26  65  professional_types\n",
              "20   6  14   8  10  20   1   5  11  27  24  right_professional\n",
              "21   6   3  10   9  27   1   5  11   0   0  right_professional"
            ]
          },
          "execution_count": 29,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df_encoded"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 30,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "kxyYd8LvXSwB",
        "outputId": "32c053a6-2222-4c09-d36d-c2ace77ed244"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "array([1, 1, 1, 0, 0, 9, 9, 9, 4, 4, 6, 6, 2, 2, 7, 7, 8, 8, 3, 3, 5, 5])"
            ]
          },
          "execution_count": 30,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "lable_enc = LabelEncoder()\n",
        "\n",
        "# encoding the labels\n",
        "\n",
        "labl = lable_enc.fit_transform(df_encoded.labels)\n",
        "labl"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 31,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "EL0qCx9e_9Jm",
        "outputId": "e7ac0310-b592-4f3d-920f-acefda9bdeba"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "22"
            ]
          },
          "execution_count": 31,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "len(labl)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 32,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "XMC_1ZukXiDL",
        "outputId": "cd90cd74-9007-4df0-d558-f07cd0e9db15"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "{'definition': 1,\n",
              " 'affects_whom': 0,\n",
              " 'what_causes': 9,\n",
              " 'recover': 4,\n",
              " 'steps': 6,\n",
              " 'find_help': 2,\n",
              " 'treatement_options': 7,\n",
              " 'treatment_tips': 8,\n",
              " 'professional_types': 3,\n",
              " 'right_professional': 5}"
            ]
          },
          "execution_count": 32,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "mapper = {}\n",
        "for index,key in enumerate(df_encoded.labels):\n",
        "    if key not in mapper.keys():\n",
        "        mapper[key] = labl[index]\n",
        "mapper"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "P3myx7GaAI5Q"
      },
      "source": [
        "Repeat the same for df2"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 33,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 203
        },
        "id": "4nCk2oQbXh_X",
        "outputId": "7fa8a86a-9bb1-40c5-9bbb-d08e0472e4f1"
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
              "      <th>response</th>\n",
              "      <th>labels</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Mental illnesses are health conditions that di...</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>It is estimated that mental illness affects 1 ...</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Symptoms of mental health disorders vary depen...</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>When healing from mental illness, early identi...</td>\n",
              "      <td>recover</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>Although this website cannot substitute for pr...</td>\n",
              "      <td>steps</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "                                            response        labels\n",
              "0  Mental illnesses are health conditions that di...    definition\n",
              "1  It is estimated that mental illness affects 1 ...  affects_whom\n",
              "2  Symptoms of mental health disorders vary depen...   what_causes\n",
              "3  When healing from mental illness, early identi...       recover\n",
              "4  Although this website cannot substitute for pr...         steps"
            ]
          },
          "execution_count": 33,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df2.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 34,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 357
        },
        "id": "5mqpR_GuMPrc",
        "outputId": "4f2363e2-0a7b-45cf-b527-e4c108400f08"
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
              "      <th>response</th>\n",
              "      <th>labels</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Mental illnesses are health conditions that di...</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>It is estimated that mental illness affects 1 ...</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Symptoms of mental health disorders vary depen...</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>When healing from mental illness, early identi...</td>\n",
              "      <td>recover</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>Although this website cannot substitute for pr...</td>\n",
              "      <td>steps</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>Feeling comfortable with the professional you ...</td>\n",
              "      <td>find_help</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>Just as there are different types of medicatio...</td>\n",
              "      <td>treatement_options</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>Since beginning treatment is a big step for in...</td>\n",
              "      <td>treatment_tips</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>There are many types of mental health professi...</td>\n",
              "      <td>professional_types</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>Feeling comfortable with the professional you ...</td>\n",
              "      <td>right_professional</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "                                            response              labels\n",
              "0  Mental illnesses are health conditions that di...          definition\n",
              "1  It is estimated that mental illness affects 1 ...        affects_whom\n",
              "2  Symptoms of mental health disorders vary depen...         what_causes\n",
              "3  When healing from mental illness, early identi...             recover\n",
              "4  Although this website cannot substitute for pr...               steps\n",
              "5  Feeling comfortable with the professional you ...           find_help\n",
              "6  Just as there are different types of medicatio...  treatement_options\n",
              "7  Since beginning treatment is a big step for in...      treatment_tips\n",
              "8  There are many types of mental health professi...  professional_types\n",
              "9  Feeling comfortable with the professional you ...  right_professional"
            ]
          },
          "execution_count": 34,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df2"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 35,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 203
        },
        "id": "cR7qqxoeXh8w",
        "outputId": "bfb288a2-e061-4928-9b8b-3a1e20d69fa2"
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
              "      <th>response</th>\n",
              "      <th>labels</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Mental illnesses are health conditions that di...</td>\n",
              "      <td>1</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>It is estimated that mental illness affects 1 ...</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Symptoms of mental health disorders vary depen...</td>\n",
              "      <td>9</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>When healing from mental illness, early identi...</td>\n",
              "      <td>4</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>Although this website cannot substitute for pr...</td>\n",
              "      <td>6</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "                                            response  labels\n",
              "0  Mental illnesses are health conditions that di...       1\n",
              "1  It is estimated that mental illness affects 1 ...       0\n",
              "2  Symptoms of mental health disorders vary depen...       9\n",
              "3  When healing from mental illness, early identi...       4\n",
              "4  Although this website cannot substitute for pr...       6"
            ]
          },
          "execution_count": 35,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df2.labels = df2.labels.map(mapper).astype({'labels': 'int32'})\n",
        "df2.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 36,
      "metadata": {
        "id": "4ixZCvNZXn4g"
      },
      "outputs": [],
      "source": [
        "df2.to_csv('response.csv',index=False)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 37,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 203
        },
        "id": "hIjUTKNvAfao",
        "outputId": "a084e1eb-af7a-49bd-c664-4453abdaf6c0"
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
              "      <th>0</th>\n",
              "      <th>1</th>\n",
              "      <th>2</th>\n",
              "      <th>3</th>\n",
              "      <th>4</th>\n",
              "      <th>5</th>\n",
              "      <th>6</th>\n",
              "      <th>7</th>\n",
              "      <th>8</th>\n",
              "      <th>9</th>\n",
              "      <th>labels</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>2</td>\n",
              "      <td>12</td>\n",
              "      <td>18</td>\n",
              "      <td>28</td>\n",
              "      <td>3</td>\n",
              "      <td>19</td>\n",
              "      <td>20</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>2</td>\n",
              "      <td>7</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>29</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>13</td>\n",
              "      <td>12</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>30</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>13</td>\n",
              "      <td>7</td>\n",
              "      <td>31</td>\n",
              "      <td>32</td>\n",
              "      <td>33</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "    0   1   2   3   4   5   6  7  8  9        labels\n",
              "0   2  12  18  28   3  19  20  1  4  0    definition\n",
              "1   2   7   1   5   4   0   0  0  0  0    definition\n",
              "2  29   1   5   4   0   0   0  0  0  0    definition\n",
              "3  13  12   1   4  30   0   0  0  0  0  affects_whom\n",
              "4  13   7  31  32  33   4   0  0  0  0  affects_whom"
            ]
          },
          "execution_count": 37,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "df_encoded.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 38,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "gIyITJXtAkHZ",
        "outputId": "59a4c91e-e020-48ad-e2d4-44587dba3534"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "[1, 2, 4, 6, 7, 9, 11, 13, 15, 17, 19, 21]"
            ]
          },
          "execution_count": 38,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "train_index"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 39,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "mdAynG8hAmUF",
        "outputId": "aff7c007-10fe-4482-d4fa-ff03e1c283d1"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "[3, 0, 12, 18, 8, 20, 10, 14, 16, 5]"
            ]
          },
          "execution_count": 39,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "test_index"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 40,
      "metadata": {
        "id": "-KWZh9SUXtwA"
      },
      "outputs": [],
      "source": [
        "train = df_encoded.loc[train_index]\n",
        "test = df_encoded.loc[test_index]"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Fb9aSpfs7NSN"
      },
      "source": [
        "## Training and testing"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 41,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 418
        },
        "id": "AcAZpSdmBYSx",
        "outputId": "001562f0-5172-4d9d-a1bc-5c57b6b84084"
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
              "      <th>0</th>\n",
              "      <th>1</th>\n",
              "      <th>2</th>\n",
              "      <th>3</th>\n",
              "      <th>4</th>\n",
              "      <th>5</th>\n",
              "      <th>6</th>\n",
              "      <th>7</th>\n",
              "      <th>8</th>\n",
              "      <th>9</th>\n",
              "      <th>labels</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>2</td>\n",
              "      <td>7</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>29</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>13</td>\n",
              "      <td>7</td>\n",
              "      <td>31</td>\n",
              "      <td>32</td>\n",
              "      <td>33</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>2</td>\n",
              "      <td>35</td>\n",
              "      <td>3</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>6</td>\n",
              "      <td>12</td>\n",
              "      <td>21</td>\n",
              "      <td>36</td>\n",
              "      <td>37</td>\n",
              "      <td>38</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>7</td>\n",
              "      <td>18</td>\n",
              "      <td>41</td>\n",
              "      <td>3</td>\n",
              "      <td>15</td>\n",
              "      <td>42</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>recover</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>11</th>\n",
              "      <td>2</td>\n",
              "      <td>16</td>\n",
              "      <td>9</td>\n",
              "      <td>47</td>\n",
              "      <td>3</td>\n",
              "      <td>48</td>\n",
              "      <td>49</td>\n",
              "      <td>50</td>\n",
              "      <td>23</td>\n",
              "      <td>22</td>\n",
              "      <td>steps</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>find_help</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>15</th>\n",
              "      <td>6</td>\n",
              "      <td>14</td>\n",
              "      <td>21</td>\n",
              "      <td>15</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>treatement_options</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>17</th>\n",
              "      <td>2</td>\n",
              "      <td>56</td>\n",
              "      <td>8</td>\n",
              "      <td>57</td>\n",
              "      <td>25</td>\n",
              "      <td>58</td>\n",
              "      <td>59</td>\n",
              "      <td>8</td>\n",
              "      <td>60</td>\n",
              "      <td>17</td>\n",
              "      <td>treatment_tips</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>19</th>\n",
              "      <td>2</td>\n",
              "      <td>16</td>\n",
              "      <td>9</td>\n",
              "      <td>63</td>\n",
              "      <td>64</td>\n",
              "      <td>23</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>26</td>\n",
              "      <td>65</td>\n",
              "      <td>professional_types</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>21</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>9</td>\n",
              "      <td>27</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>right_professional</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "     0   1   2   3   4   5   6   7   8   9              labels\n",
              "1    2   7   1   5   4   0   0   0   0   0          definition\n",
              "2   29   1   5   4   0   0   0   0   0   0          definition\n",
              "4   13   7  31  32  33   4   0   0   0   0        affects_whom\n",
              "6    2  35   3   1   4   0   0   0   0   0         what_causes\n",
              "7    6  12  21  36  37  38   0   0   0   0         what_causes\n",
              "9    7  18  41   3  15  42   1   4   0   0             recover\n",
              "11   2  16   9  47   3  48  49  50  23  22               steps\n",
              "13   6   3  10   1   5  11   0   0   0   0           find_help\n",
              "15   6  14  21  15   0   0   0   0   0   0  treatement_options\n",
              "17   2  56   8  57  25  58  59   8  60  17      treatment_tips\n",
              "19   2  16   9  63  64  23   1   5  26  65  professional_types\n",
              "21   6   3  10   9  27   1   5  11   0   0  right_professional"
            ]
          },
          "execution_count": 41,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "train"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 42,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 203
        },
        "id": "epPEROQGBlsm",
        "outputId": "20e37b06-0375-4ce9-82d2-0a4cb57bec53"
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
              "      <th>0</th>\n",
              "      <th>1</th>\n",
              "      <th>2</th>\n",
              "      <th>3</th>\n",
              "      <th>4</th>\n",
              "      <th>5</th>\n",
              "      <th>6</th>\n",
              "      <th>7</th>\n",
              "      <th>8</th>\n",
              "      <th>9</th>\n",
              "      <th>labels</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>13</td>\n",
              "      <td>12</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>30</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>2</td>\n",
              "      <td>12</td>\n",
              "      <td>18</td>\n",
              "      <td>28</td>\n",
              "      <td>3</td>\n",
              "      <td>19</td>\n",
              "      <td>20</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>12</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>51</td>\n",
              "      <td>24</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>find_help</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>18</th>\n",
              "      <td>2</td>\n",
              "      <td>7</td>\n",
              "      <td>9</td>\n",
              "      <td>61</td>\n",
              "      <td>62</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>26</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>professional_types</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>14</td>\n",
              "      <td>39</td>\n",
              "      <td>40</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>15</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>recover</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "     0   1   2   3   4   5   6   7  8  9              labels\n",
              "3   13  12   1   4  30   0   0   0  0  0        affects_whom\n",
              "0    2  12  18  28   3  19  20   1  4  0          definition\n",
              "12   6   3  10   1   5  11  51  24  0  0           find_help\n",
              "18   2   7   9  61  62   1   5  26  0  0  professional_types\n",
              "8   14  39  40   1   4  15   0   0  0  0             recover"
            ]
          },
          "execution_count": 42,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "test.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 43,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "C1ZYcCJFmQfg",
        "outputId": "3726982d-8103-4c01-c4ac-cb1cc22665d5"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "labels\n",
              "definition            2\n",
              "what_causes           2\n",
              "affects_whom          1\n",
              "recover               1\n",
              "steps                 1\n",
              "find_help             1\n",
              "treatement_options    1\n",
              "treatment_tips        1\n",
              "professional_types    1\n",
              "right_professional    1\n",
              "Name: count, dtype: int64"
            ]
          },
          "execution_count": 43,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "train.labels.value_counts()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 44,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "E46URbzfmTLE",
        "outputId": "6f923aae-c043-43e7-d209-94ff07b7881e"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "labels\n",
              "affects_whom          1\n",
              "definition            1\n",
              "find_help             1\n",
              "professional_types    1\n",
              "recover               1\n",
              "right_professional    1\n",
              "steps                 1\n",
              "treatement_options    1\n",
              "treatment_tips        1\n",
              "what_causes           1\n",
              "Name: count, dtype: int64"
            ]
          },
          "execution_count": 44,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "test.labels.value_counts()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 45,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 418
        },
        "id": "PcbjQwN-RQui",
        "outputId": "0eebccd7-fa8c-4bdf-cedc-c8bd68ce066d"
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
              "      <th>0</th>\n",
              "      <th>1</th>\n",
              "      <th>2</th>\n",
              "      <th>3</th>\n",
              "      <th>4</th>\n",
              "      <th>5</th>\n",
              "      <th>6</th>\n",
              "      <th>7</th>\n",
              "      <th>8</th>\n",
              "      <th>9</th>\n",
              "      <th>labels</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>2</td>\n",
              "      <td>7</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>29</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>definition</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>13</td>\n",
              "      <td>7</td>\n",
              "      <td>31</td>\n",
              "      <td>32</td>\n",
              "      <td>33</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>affects_whom</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>2</td>\n",
              "      <td>35</td>\n",
              "      <td>3</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>6</td>\n",
              "      <td>12</td>\n",
              "      <td>21</td>\n",
              "      <td>36</td>\n",
              "      <td>37</td>\n",
              "      <td>38</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>what_causes</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>7</td>\n",
              "      <td>18</td>\n",
              "      <td>41</td>\n",
              "      <td>3</td>\n",
              "      <td>15</td>\n",
              "      <td>42</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>recover</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>11</th>\n",
              "      <td>2</td>\n",
              "      <td>16</td>\n",
              "      <td>9</td>\n",
              "      <td>47</td>\n",
              "      <td>3</td>\n",
              "      <td>48</td>\n",
              "      <td>49</td>\n",
              "      <td>50</td>\n",
              "      <td>23</td>\n",
              "      <td>22</td>\n",
              "      <td>steps</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>find_help</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>15</th>\n",
              "      <td>6</td>\n",
              "      <td>14</td>\n",
              "      <td>21</td>\n",
              "      <td>15</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>treatement_options</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>17</th>\n",
              "      <td>2</td>\n",
              "      <td>56</td>\n",
              "      <td>8</td>\n",
              "      <td>57</td>\n",
              "      <td>25</td>\n",
              "      <td>58</td>\n",
              "      <td>59</td>\n",
              "      <td>8</td>\n",
              "      <td>60</td>\n",
              "      <td>17</td>\n",
              "      <td>treatment_tips</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>19</th>\n",
              "      <td>2</td>\n",
              "      <td>16</td>\n",
              "      <td>9</td>\n",
              "      <td>63</td>\n",
              "      <td>64</td>\n",
              "      <td>23</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>26</td>\n",
              "      <td>65</td>\n",
              "      <td>professional_types</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>21</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>9</td>\n",
              "      <td>27</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>right_professional</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "     0   1   2   3   4   5   6   7   8   9              labels\n",
              "1    2   7   1   5   4   0   0   0   0   0          definition\n",
              "2   29   1   5   4   0   0   0   0   0   0          definition\n",
              "4   13   7  31  32  33   4   0   0   0   0        affects_whom\n",
              "6    2  35   3   1   4   0   0   0   0   0         what_causes\n",
              "7    6  12  21  36  37  38   0   0   0   0         what_causes\n",
              "9    7  18  41   3  15  42   1   4   0   0             recover\n",
              "11   2  16   9  47   3  48  49  50  23  22               steps\n",
              "13   6   3  10   1   5  11   0   0   0   0           find_help\n",
              "15   6  14  21  15   0   0   0   0   0   0  treatement_options\n",
              "17   2  56   8  57  25  58  59   8  60  17      treatment_tips\n",
              "19   2  16   9  63  64  23   1   5  26  65  professional_types\n",
              "21   6   3  10   9  27   1   5  11   0   0  right_professional"
            ]
          },
          "execution_count": 45,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "train"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 46,
      "metadata": {
        "id": "G2syG8OIXtsl"
      },
      "outputs": [],
      "source": [
        "X_train = train.drop(columns=['labels'],axis=1)\n",
        "y_train = train.labels\n",
        "X_test = test.drop(columns=['labels'],axis=1)\n",
        "y_test = test.labels"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 47,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 203
        },
        "id": "t0jjLEnErX9h",
        "outputId": "e444ff00-cc70-405f-ebdf-61fee0a57de7"
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
              "      <th>0</th>\n",
              "      <th>1</th>\n",
              "      <th>2</th>\n",
              "      <th>3</th>\n",
              "      <th>4</th>\n",
              "      <th>5</th>\n",
              "      <th>6</th>\n",
              "      <th>7</th>\n",
              "      <th>8</th>\n",
              "      <th>9</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>2</td>\n",
              "      <td>7</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>29</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>13</td>\n",
              "      <td>7</td>\n",
              "      <td>31</td>\n",
              "      <td>32</td>\n",
              "      <td>33</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>2</td>\n",
              "      <td>35</td>\n",
              "      <td>3</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>6</td>\n",
              "      <td>12</td>\n",
              "      <td>21</td>\n",
              "      <td>36</td>\n",
              "      <td>37</td>\n",
              "      <td>38</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "    0   1   2   3   4   5  6  7  8  9\n",
              "1   2   7   1   5   4   0  0  0  0  0\n",
              "2  29   1   5   4   0   0  0  0  0  0\n",
              "4  13   7  31  32  33   4  0  0  0  0\n",
              "6   2  35   3   1   4   0  0  0  0  0\n",
              "7   6  12  21  36  37  38  0  0  0  0"
            ]
          },
          "execution_count": 47,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "X_train.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 48,
      "metadata": {
        "id": "1cSOF7OeXtqJ"
      },
      "outputs": [],
      "source": [
        "y_train =pd.get_dummies(y_train).values\n",
        "y_test =pd.get_dummies(y_test).values"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 49,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 357
        },
        "id": "lG_4kPvW96KK",
        "outputId": "953e0046-fa67-4b93-8c56-af3ecde9abb5"
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
              "      <th>0</th>\n",
              "      <th>1</th>\n",
              "      <th>2</th>\n",
              "      <th>3</th>\n",
              "      <th>4</th>\n",
              "      <th>5</th>\n",
              "      <th>6</th>\n",
              "      <th>7</th>\n",
              "      <th>8</th>\n",
              "      <th>9</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>13</td>\n",
              "      <td>12</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>30</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>2</td>\n",
              "      <td>12</td>\n",
              "      <td>18</td>\n",
              "      <td>28</td>\n",
              "      <td>3</td>\n",
              "      <td>19</td>\n",
              "      <td>20</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>12</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>51</td>\n",
              "      <td>24</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>18</th>\n",
              "      <td>2</td>\n",
              "      <td>7</td>\n",
              "      <td>9</td>\n",
              "      <td>61</td>\n",
              "      <td>62</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>26</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>14</td>\n",
              "      <td>39</td>\n",
              "      <td>40</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>15</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>20</th>\n",
              "      <td>6</td>\n",
              "      <td>14</td>\n",
              "      <td>8</td>\n",
              "      <td>10</td>\n",
              "      <td>20</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>27</td>\n",
              "      <td>24</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>10</th>\n",
              "      <td>8</td>\n",
              "      <td>43</td>\n",
              "      <td>44</td>\n",
              "      <td>13</td>\n",
              "      <td>45</td>\n",
              "      <td>3</td>\n",
              "      <td>19</td>\n",
              "      <td>46</td>\n",
              "      <td>22</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>14</th>\n",
              "      <td>2</td>\n",
              "      <td>17</td>\n",
              "      <td>52</td>\n",
              "      <td>16</td>\n",
              "      <td>53</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>16</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>54</td>\n",
              "      <td>55</td>\n",
              "      <td>25</td>\n",
              "      <td>17</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>2</td>\n",
              "      <td>34</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "     0   1   2   3   4   5   6   7   8   9\n",
              "3   13  12   1   4  30   0   0   0   0   0\n",
              "0    2  12  18  28   3  19  20   1   4   0\n",
              "12   6   3  10   1   5  11  51  24   0   0\n",
              "18   2   7   9  61  62   1   5  26   0   0\n",
              "8   14  39  40   1   4  15   0   0   0   0\n",
              "20   6  14   8  10  20   1   5  11  27  24\n",
              "10   8  43  44  13  45   3  19  46  22   0\n",
              "14   2  17  52  16  53   0   0   0   0   0\n",
              "16   6   3  54  55  25  17   0   0   0   0\n",
              "5    2  34   1   4   0   0   0   0   0   0"
            ]
          },
          "execution_count": 49,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "X_test"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 50,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 418
        },
        "id": "bZyNYXsjfY2y",
        "outputId": "6e462b54-5e0c-45d6-a911-e361be113c6c"
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
              "      <th>0</th>\n",
              "      <th>1</th>\n",
              "      <th>2</th>\n",
              "      <th>3</th>\n",
              "      <th>4</th>\n",
              "      <th>5</th>\n",
              "      <th>6</th>\n",
              "      <th>7</th>\n",
              "      <th>8</th>\n",
              "      <th>9</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>2</td>\n",
              "      <td>7</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>29</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>13</td>\n",
              "      <td>7</td>\n",
              "      <td>31</td>\n",
              "      <td>32</td>\n",
              "      <td>33</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>2</td>\n",
              "      <td>35</td>\n",
              "      <td>3</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>6</td>\n",
              "      <td>12</td>\n",
              "      <td>21</td>\n",
              "      <td>36</td>\n",
              "      <td>37</td>\n",
              "      <td>38</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>7</td>\n",
              "      <td>18</td>\n",
              "      <td>41</td>\n",
              "      <td>3</td>\n",
              "      <td>15</td>\n",
              "      <td>42</td>\n",
              "      <td>1</td>\n",
              "      <td>4</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>11</th>\n",
              "      <td>2</td>\n",
              "      <td>16</td>\n",
              "      <td>9</td>\n",
              "      <td>47</td>\n",
              "      <td>3</td>\n",
              "      <td>48</td>\n",
              "      <td>49</td>\n",
              "      <td>50</td>\n",
              "      <td>23</td>\n",
              "      <td>22</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>15</th>\n",
              "      <td>6</td>\n",
              "      <td>14</td>\n",
              "      <td>21</td>\n",
              "      <td>15</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>17</th>\n",
              "      <td>2</td>\n",
              "      <td>56</td>\n",
              "      <td>8</td>\n",
              "      <td>57</td>\n",
              "      <td>25</td>\n",
              "      <td>58</td>\n",
              "      <td>59</td>\n",
              "      <td>8</td>\n",
              "      <td>60</td>\n",
              "      <td>17</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>19</th>\n",
              "      <td>2</td>\n",
              "      <td>16</td>\n",
              "      <td>9</td>\n",
              "      <td>63</td>\n",
              "      <td>64</td>\n",
              "      <td>23</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>26</td>\n",
              "      <td>65</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>21</th>\n",
              "      <td>6</td>\n",
              "      <td>3</td>\n",
              "      <td>10</td>\n",
              "      <td>9</td>\n",
              "      <td>27</td>\n",
              "      <td>1</td>\n",
              "      <td>5</td>\n",
              "      <td>11</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "     0   1   2   3   4   5   6   7   8   9\n",
              "1    2   7   1   5   4   0   0   0   0   0\n",
              "2   29   1   5   4   0   0   0   0   0   0\n",
              "4   13   7  31  32  33   4   0   0   0   0\n",
              "6    2  35   3   1   4   0   0   0   0   0\n",
              "7    6  12  21  36  37  38   0   0   0   0\n",
              "9    7  18  41   3  15  42   1   4   0   0\n",
              "11   2  16   9  47   3  48  49  50  23  22\n",
              "13   6   3  10   1   5  11   0   0   0   0\n",
              "15   6  14  21  15   0   0   0   0   0   0\n",
              "17   2  56   8  57  25  58  59   8  60  17\n",
              "19   2  16   9  63  64  23   1   5  26  65\n",
              "21   6   3  10   9  27   1   5  11   0   0"
            ]
          },
          "execution_count": 50,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "X_train"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 51,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "wWFWgav5B-pH",
        "outputId": "cb4ed15f-5382-476e-a2f8-cf55f306ae84"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "array([[False,  True, False, False, False, False, False, False, False,\n",
              "        False],\n",
              "       [False,  True, False, False, False, False, False, False, False,\n",
              "        False],\n",
              "       [ True, False, False, False, False, False, False, False, False,\n",
              "        False],\n",
              "       [False, False, False, False, False, False, False, False, False,\n",
              "         True],\n",
              "       [False, False, False, False, False, False, False, False, False,\n",
              "         True],\n",
              "       [False, False, False, False,  True, False, False, False, False,\n",
              "        False],\n",
              "       [False, False, False, False, False, False,  True, False, False,\n",
              "        False],\n",
              "       [False, False,  True, False, False, False, False, False, False,\n",
              "        False],\n",
              "       [False, False, False, False, False, False, False,  True, False,\n",
              "        False],\n",
              "       [False, False, False, False, False, False, False, False,  True,\n",
              "        False],\n",
              "       [False, False, False,  True, False, False, False, False, False,\n",
              "        False],\n",
              "       [False, False, False, False, False,  True, False, False, False,\n",
              "        False]])"
            ]
          },
          "execution_count": 51,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "y_train"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 52,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "xvhKy5u6mM0k",
        "outputId": "2c3889ca-337e-4cad-be92-984234f8ed31"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "array([False,  True, False, False, False, False, False, False, False,\n",
              "       False])"
            ]
          },
          "execution_count": 52,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "y_train[0]"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 53,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "pPZDWFkBmOdx",
        "outputId": "5ae5e495-7ca3-4f7c-8ed7-4d6af7a3413b"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "array([[ True, False, False, False, False, False, False, False, False,\n",
              "        False],\n",
              "       [False,  True, False, False, False, False, False, False, False,\n",
              "        False],\n",
              "       [False, False,  True, False, False, False, False, False, False,\n",
              "        False],\n",
              "       [False, False, False,  True, False, False, False, False, False,\n",
              "        False],\n",
              "       [False, False, False, False,  True, False, False, False, False,\n",
              "        False],\n",
              "       [False, False, False, False, False,  True, False, False, False,\n",
              "        False],\n",
              "       [False, False, False, False, False, False,  True, False, False,\n",
              "        False],\n",
              "       [False, False, False, False, False, False, False,  True, False,\n",
              "        False],\n",
              "       [False, False, False, False, False, False, False, False,  True,\n",
              "        False],\n",
              "       [False, False, False, False, False, False, False, False, False,\n",
              "         True]])"
            ]
          },
          "execution_count": 53,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "y_test"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 54,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "X_urYiDyXtn5",
        "outputId": "bd674f43-900b-410a-d670-309243eac8ae"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "((10,), (10,))"
            ]
          },
          "execution_count": 54,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "y_train[0].shape,y_test[0].shape"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 55,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "0jMrfnwKX1DC",
        "outputId": "832af3f7-4495-4c08-b90c-c97eff02dabf"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "(12, 10)"
            ]
          },
          "execution_count": 55,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "X_train.shape"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 56,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Yf1it_OmmurY",
        "outputId": "d3e15ac4-58c1-4ce6-d228-7b380c988c78"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "(10, 10)"
            ]
          },
          "execution_count": 56,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "X_test.shape"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 57,
      "metadata": {
        "id": "fJHi-DiIX0_D"
      },
      "outputs": [],
      "source": [
        "max_length = X_train.shape[1]\n",
        "output = 16                  # no of classes"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "v72uEhyGCk8Z"
      },
      "source": [
        "Reference for the model below:\n",
        "\n",
        "*   https://keras.io/api/callbacks/model_checkpoint/\n",
        "*   https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/ReduceLROnPlateau"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 58,
      "metadata": {
        "id": "QtCFWykAX08b"
      },
      "outputs": [],
      "source": [
        "early_stopping = EarlyStopping(monitor='val_loss',patience=10) #patience : number of epochs with no improvement after which training will be stopped\n",
        "\n",
        "checkpoint = ModelCheckpoint(\"model-v1.h5\",\n",
        "                             monitor=\"val_loss\",\n",
        "                             mode=\"min\",\n",
        "                             save_best_only = True,\n",
        "                             verbose=1)\n",
        "\n",
        "reduce_lr = ReduceLROnPlateau(monitor = 'val_loss', factor = 0.2, patience = 3, verbose = 1, min_delta = 0.0001)\n",
        "\n",
        "callbacks = [early_stopping,checkpoint,reduce_lr]"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "65wJtH4MG0It"
      },
      "source": [
        "References : \n",
        "* Word embeddings - https://machinelearningmastery.com/use-word-embedding-layers-deep-learning-keras/\n",
        "* 2D CNN when we have 3D features, such as RGB - \n",
        "https://missinglink.ai/guides/keras/keras-conv1d-working-1d-convolutional-neural-networks-keras/\n",
        "* Pooling layers reduce the size of the representation to speed up the computation and make features robust\n",
        "* Add a \"flatten\" layer which prepares a vector for the fully connected layers, for example using Sequential.add(Flatten()) -  \n",
        "https://missinglink.ai/guides/keras/using-keras-flatten-operation-cnn-models-code-examples/\n",
        "* Dense layer - A fully connected layer also known as the dense layer, in which the results of the convolutional layers are fed through one or more neural layers to generate a prediction\n",
        "* Activation functions - https://towardsdatascience.com/activation-functions-neural-networks-1cbd9f8d91d6 "
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "5zfZy2tABMkl"
      },
      "source": [
        "## Vanilla RNN"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "6uwe7aPetEi3"
      },
      "source": [
        "* Why use embedding layer before RNN/ LSTM layer -\n",
        "https://towardsdatascience.com/deep-learning-4-embedding-layers-f9a02d55ac12\n",
        "* Learning curves - https://www.dataquest.io/blog/learning-curves-machine-learning/\n",
        "\n",
        "\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 59,
      "metadata": {
        "id": "AOvE1ucyMcUZ"
      },
      "outputs": [],
      "source": [
        "def define_model1(vocab_size, max_length):\n",
        "    model1 = Sequential()\n",
        "    model1.add(Embedding(vocab_size,100, input_length=max_length))\n",
        "    model1.add(SimpleRNN(100))\n",
        "    model1.add(Dense(10, activation='softmax'))   \n",
        "    \n",
        "    model1.compile(loss = 'categorical_crossentropy',optimizer = 'adam',metrics = ['accuracy'])\n",
        "    \n",
        "    # summarize defined model\n",
        "    model1.summary()\n",
        "    plot_model(model1, to_file='model_1.png', show_shapes=True)\n",
        "    return model1"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 60,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Toir2G_NNEsX",
        "outputId": "98112820-925a-41a4-eea9-28ac0da91f8d"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Model: \"sequential\"\n",
            "_________________________________________________________________\n",
            " Layer (type)                Output Shape              Param #   \n",
            "=================================================================\n",
            " embedding (Embedding)       (None, 10, 100)           6600      \n",
            "                                                                 \n",
            " simple_rnn (SimpleRNN)      (None, 100)               20100     \n",
            "                                                                 \n",
            " dense (Dense)               (None, 10)                1010      \n",
            "                                                                 \n",
            "=================================================================\n",
            "Total params: 27710 (108.24 KB)\n",
            "Trainable params: 27710 (108.24 KB)\n",
            "Non-trainable params: 0 (0.00 Byte)\n",
            "_________________________________________________________________\n",
            "You must install pydot (`pip install pydot`) and install graphviz (see instructions at https://graphviz.gitlab.io/download/) for plot_model to work.\n"
          ]
        }
      ],
      "source": [
        "model1 = define_model1(vocab_size, max_length)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 61,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "pTFpfCkUNEpg",
        "outputId": "9191868b-6612-4c08-c99b-1babf28333bb"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Epoch 1/10\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.3133 - accuracy: 0.0000e+00\n",
            "Epoch 1: val_loss improved from inf to 2.24612, saving model to model-v1.h5\n",
            "1/1 [==============================] - 1s 858ms/step - loss: 2.3133 - accuracy: 0.0000e+00 - val_loss: 2.2461 - val_accuracy: 0.1000 - lr: 0.0010\n",
            "Epoch 2/10\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.1745 - accuracy: 0.3333\n",
            "Epoch 2: val_loss improved from 2.24612 to 2.22545, saving model to model-v1.h5\n",
            "1/1 [==============================] - 0s 30ms/step - loss: 2.1745 - accuracy: 0.3333 - val_loss: 2.2255 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 3/10\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.0396 - accuracy: 0.8333\n",
            "Epoch 3: val_loss improved from 2.22545 to 2.20654, saving model to model-v1.h5\n",
            "1/1 [==============================] - 0s 44ms/step - loss: 2.0396 - accuracy: 0.8333 - val_loss: 2.2065 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 4/10\n",
            "1/1 [==============================] - ETA: 0s - loss: 1.9062 - accuracy: 0.8333\n",
            "Epoch 4: val_loss improved from 2.20654 to 2.18922, saving model to model-v1.h5\n",
            "1/1 [==============================] - 0s 32ms/step - loss: 1.9062 - accuracy: 0.8333 - val_loss: 2.1892 - val_accuracy: 0.1000 - lr: 0.0010\n",
            "Epoch 5/10\n",
            "1/1 [==============================] - ETA: 0s - loss: 1.7727 - accuracy: 0.9167\n",
            "Epoch 5: val_loss improved from 2.18922 to 2.17344, saving model to model-v1.h5\n",
            "1/1 [==============================] - 0s 42ms/step - loss: 1.7727 - accuracy: 0.9167 - val_loss: 2.1734 - val_accuracy: 0.1000 - lr: 0.0010\n",
            "Epoch 6/10\n",
            "1/1 [==============================] - ETA: 0s - loss: 1.6380 - accuracy: 0.9167\n",
            "Epoch 6: val_loss improved from 2.17344 to 2.15924, saving model to model-v1.h5\n",
            "1/1 [==============================] - 0s 33ms/step - loss: 1.6380 - accuracy: 0.9167 - val_loss: 2.1592 - val_accuracy: 0.1000 - lr: 0.0010\n",
            "Epoch 7/10\n"
          ]
        },
        {
          "name": "stderr",
          "output_type": "stream",
          "text": [
            "/Users/anuradha.pandey/anaconda3/envs/mental_health/lib/python3.8/site-packages/keras/src/engine/training.py:3000: UserWarning: You are saving your model as an HDF5 file via `model.save()`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')`.\n",
            "  saving_api.save_model(\n"
          ]
        },
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "1/1 [==============================] - ETA: 0s - loss: 1.5020 - accuracy: 0.9167\n",
            "Epoch 7: val_loss improved from 2.15924 to 2.14641, saving model to model-v1.h5\n",
            "1/1 [==============================] - 0s 26ms/step - loss: 1.5020 - accuracy: 0.9167 - val_loss: 2.1464 - val_accuracy: 0.1000 - lr: 0.0010\n",
            "Epoch 8/10\n",
            "1/1 [==============================] - ETA: 0s - loss: 1.3643 - accuracy: 1.0000\n",
            "Epoch 8: val_loss improved from 2.14641 to 2.13428, saving model to model-v1.h5\n",
            "1/1 [==============================] - 0s 26ms/step - loss: 1.3643 - accuracy: 1.0000 - val_loss: 2.1343 - val_accuracy: 0.1000 - lr: 0.0010\n",
            "Epoch 9/10\n",
            "1/1 [==============================] - ETA: 0s - loss: 1.2253 - accuracy: 1.0000\n",
            "Epoch 9: val_loss improved from 2.13428 to 2.12216, saving model to model-v1.h5\n",
            "1/1 [==============================] - 0s 26ms/step - loss: 1.2253 - accuracy: 1.0000 - val_loss: 2.1222 - val_accuracy: 0.1000 - lr: 0.0010\n",
            "Epoch 10/10\n",
            "1/1 [==============================] - ETA: 0s - loss: 1.0853 - accuracy: 1.0000\n",
            "Epoch 10: val_loss improved from 2.12216 to 2.10980, saving model to model-v1.h5\n",
            "1/1 [==============================] - 0s 25ms/step - loss: 1.0853 - accuracy: 1.0000 - val_loss: 2.1098 - val_accuracy: 0.1000 - lr: 0.0010\n"
          ]
        }
      ],
      "source": [
        "history1 = model1.fit(X_train, y_train, epochs=10, verbose=1,validation_data=(X_test,y_test),callbacks=callbacks)#,callbacks=callbacks)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 62,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 513
        },
        "id": "k0I_FjV6mDQR",
        "outputId": "647955ed-729d-432f-b78f-52d08bf8798d"
      },
      "outputs": [
        {
          "data": {
            "image/png": "iVBORw0KGgoAAAANSUhEUgAABR8AAAK9CAYAAACtshu3AAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8WgzjOAAAACXBIWXMAAA9hAAAPYQGoP6dpAADqCUlEQVR4nOzdd3gU5frG8Xs3ZdMTSCMk9F5CkSaggOegFOWIIiLSm9Js2I+K4lH42QsWVHpTFAEbiohgAaSX0FvovaT33fn9sWQhJPSESfl+rmuuJLMzs/cm0QzPvu/7WAzDMAQAAAAAAAAA+cxqdgAAAAAAAAAAxRPFRwAAAAAAAAAFguIjAAAAAAAAgAJB8REAAAAAAABAgaD4CAAAAAAAAKBAUHwEAAAAAAAAUCAoPgIAAAAAAAAoEBQfAQAAAAAAABQIio8AAAAAAAAACgTFR6AI6Nu3rypWrHhN577yyiuyWCz5G6iQ2bt3rywWiyZPnnzDn9tiseiVV15xfT158mRZLBbt3bv3sudWrFhRffv2zdc81/O7AgAAcKNwf3tp3N+ew/0tUPRRfASug8ViuaJtyZIlZkct8R599FFZLBbt2rXrose88MILslgs2rhx4w1MdvUOHz6sV155RevXrzc7Sp62bt0qi8UiLy8vxcXFmR0HAABcBe5viw7ubwtWdgH47bffNjsKUOS5mx0AKMqmTZuW4+upU6dq4cKFufbXqlXrup7niy++kMPhuKZzX3zxRT333HPX9fzFQY8ePTR27FjNnDlTI0eOzPOYL7/8UtHR0apXr941P0+vXr30wAMPyGazXfM1Lufw4cMaNWqUKlasqAYNGuR47Hp+V/LL9OnTVaZMGZ05c0azZ8/WwIEDTc0DAACuHPe3RQf3twCKCoqPwHXo2bNnjq//+ecfLVy4MNf+C6WkpMjHx+eKn8fDw+Oa8kmSu7u73N35T71Zs2aqWrWqvvzyyzxvzpYvX67Y2Fj93//933U9j5ubm9zc3K7rGtfjen5X8oNhGJo5c6YefPBBxcbGasaMGYW2+JicnCxfX1+zYwAAUKhwf1t0cH8LoKhg2jVQwNq0aaO6detqzZo1atWqlXx8fPTf//5XkvTdd9/pzjvvVNmyZWWz2VSlShX973//k91uz3GNC9c5OX8KwOeff64qVarIZrOpSZMmWrVqVY5z81oTx2KxaPjw4Zo3b57q1q0rm82mOnXq6JdffsmVf8mSJWrcuLG8vLxUpUoVffbZZ1e8zs5ff/2lrl27qnz58rLZbCpXrpyeeOIJpaam5np9fn5+OnTokDp37iw/Pz+FhobqqaeeyvW9iIuLU9++fRUYGKigoCD16dPniqf29ujRQ9u2bdPatWtzPTZz5kxZLBZ1795dGRkZGjlypBo1aqTAwED5+vrq1ltv1eLFiy/7HHmtiWMYhl577TVFRUXJx8dHt912mzZv3pzr3NOnT+upp55SdHS0/Pz8FBAQoA4dOmjDhg2uY5YsWaImTZpIkvr16+ea+pS9HlBea+IkJyfrySefVLly5WSz2VSjRg29/fbbMgwjx3FX83txMUuXLtXevXv1wAMP6IEHHtCff/6pgwcP5jrO4XDogw8+UHR0tLy8vBQaGqr27dtr9erVOY6bPn26mjZtKh8fH5UqVUqtWrXSr7/+miPz+WsSZbtwvaHsn8sff/yhoUOHKiwsTFFRUZKkffv2aejQoapRo4a8vb0VHBysrl275rmuUVxcnJ544glVrFhRNptNUVFR6t27t06ePKmkpCT5+vrqsccey3XewYMH5ebmpjFjxlzhdxIAgMKL+1vub0vS/e3lHD9+XAMGDFB4eLi8vLxUv359TZkyJddxX331lRo1aiR/f38FBAQoOjpaH3zwgevxzMxMjRo1StWqVZOXl5eCg4N1yy23aOHChfmWFTALbxcBN8CpU6fUoUMHPfDAA+rZs6fCw8MlOf+Q+/n5acSIEfLz89Pvv/+ukSNHKiEhQW+99dZlrztz5kwlJibq4YcflsVi0Ztvvql7771Xe/bsuew7hH///bfmzJmjoUOHyt/fXx9++KG6dOmi/fv3Kzg4WJK0bt06tW/fXhERERo1apTsdrteffVVhYaGXtHr/uabb5SSkqIhQ4YoODhYK1eu1NixY3Xw4EF98803OY612+1q166dmjVrprffflu//fab3nnnHVWpUkVDhgyR5LzJufvuu/X3339r8ODBqlWrlubOnas+ffpcUZ4ePXpo1KhRmjlzpm666aYcz/3111/r1ltvVfny5XXy5EmNHz9e3bt316BBg5SYmKgJEyaoXbt2WrlyZa6pIJczcuRIvfbaa+rYsaM6duyotWvX6o477lBGRkaO4/bs2aN58+apa9euqlSpko4dO6bPPvtMrVu31pYtW1S2bFnVqlVLr776qkaOHKmHHnpIt956qySpRYsWeT63YRj6z3/+o8WLF2vAgAFq0KCBFixYoKefflqHDh3Se++9l+P4K/m9uJQZM2aoSpUqatKkierWrSsfHx99+eWXevrpp3McN2DAAE2ePFkdOnTQwIEDlZWVpb/++kv//POPGjduLEkaNWqUXnnlFbVo0UKvvvqqPD09tWLFCv3++++64447rvj7f76hQ4cqNDRUI0eOVHJysiRp1apVWrZsmR544AFFRUVp7969+vTTT9WmTRtt2bLFNYojKSlJt956q7Zu3ar+/fvrpptu0smTJ/X999/r4MGDatCgge655x7NmjVL7777bo4RAl9++aUMw1CPHj2uKTcAAIUN97fc35aU+9tLSU1NVZs2bbRr1y4NHz5clSpV0jfffKO+ffsqLi7O9ab0woUL1b17d/373//WG2+8Icm5TvrSpUtdx7zyyisaM2aMBg4cqKZNmyohIUGrV6/W2rVrdfvtt19XTsB0BoB8M2zYMOPC/6xat25tSDLGjRuX6/iUlJRc+x5++GHDx8fHSEtLc+3r06ePUaFCBdfXsbGxhiQjODjYOH36tGv/d999Z0gyfvjhB9e+l19+OVcmSYanp6exa9cu174NGzYYkoyxY8e69nXq1Mnw8fExDh065Nq3c+dOw93dPdc185LX6xszZoxhsViMffv25Xh9koxXX301x7ENGzY0GjVq5Pp63rx5hiTjzTffdO3Lysoybr31VkOSMWnSpMtmatKkiREVFWXY7XbXvl9++cWQZHz22Weua6anp+c478yZM0Z4eLjRv3//HPslGS+//LLr60mTJhmSjNjYWMMwDOP48eOGp6enceeddxoOh8N13H//+19DktGnTx/XvrS0tBy5DMP5s7bZbDm+N6tWrbro673wdyX7e/baa6/lOO6+++4zLBZLjt+BK/29uJiMjAwjODjYeOGFF1z7HnzwQaN+/fo5jvv9998NScajjz6a6xrZ36OdO3caVqvVuOeee3J9T87/Pl74/c9WoUKFHN/b7J/LLbfcYmRlZeU4Nq/f0+XLlxuSjKlTp7r2jRw50pBkzJkz56K5FyxYYEgyfv755xyP16tXz2jdunWu8wAAKOy4v7386+P+1qm43d9m/06+9dZbFz3m/fffNyQZ06dPd+3LyMgw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0iTVqlVLH3zwgebNm6fbbrvtml9r3759tXPnTn3//fcKCAjQs88+q44dO2rLli3y8PDQsGHDlJGRoT///FO+vr7asmWLa3ToSy+9pC1btujnn39WSEiIdu3apdTU1GvOUpAoPgIAAAAAAKBQePXVV3X77be7vi5durTq16/v+vp///uf5s6dq++//17Dhw+/6HX69u2r7t27S5JGjx6tDz/8UCtXrlT79u3zPD4zM1Pjxo1TlSpVJEnDhw/Xq6++6np87Nixev7553XPPfdIkj766CPXKMRrkV10XLp0qVq0aCFJmjFjhsqVK6d58+apa9eu2r9/v7p06aLo6GhJUuXKlV3n79+/Xw0bNlTjxo0lOUd/FlYUHwEAAAAAAIo4bw83bXm1nWnPnV+yi2nZkpKS9Morr+inn37SkSNHlJWVpdTUVO3fv/+S16lXr57rc19fXwUEBOj48eMXPd7Hx8dVeJSkiIgI1/Hx8fE6duyYmjZt6nrczc1NjRo1ksPhuKrXl23r1q1yd3dXs2bNXPuCg4NVo0YNbd26VZL06KOPasiQIfr111/Vtm1bdenSxfW6hgwZoi5dumjt2rW644471LlzZ1cRs7BhzUcAAAAAAIAizmKxyMfT3ZTNYrHk2+vw9fXN8fVTTz2luXPnavTo0frrr7+0fv16RUdHKyMj45LX8fDwyPX9uVShMK/jr3Qty4IycOBA7dmzR7169VJMTIwaN26ssWPHSpI6dOigffv26YknntDhw4f173//W0899ZSpeS+G4iMAAAAAAAAKpaVLl6pv37665557FB0drTJlymjv3r03NENgYKDCw8O1atUq1z673a61a9de8zVr1aqlrKwsrVixwrXv1KlT2r59u2rXru3aV65cOQ0ePFhz5szRk08+qS+++ML1WGhoqPr06aPp06fr/fff1+eff37NeQoS064BAAAAAABQKFWrVk1z5sxRp06dZLFY9NJLL13zVOfr8cgjj2jMmDGqWrWqatasqbFjx+rMmTNXNOozJiZG/v7+rq8tFovq16+vu+++W4MGDdJnn30mf39/Pffcc4qMjNTdd98tSXr88cfVoUMHVa9eXWfOnNHixYtVq1YtSdLIkSPVqFEj1alTR+np6frxxx9djxU2FB8BAAAAAABQKL377rvq37+/WrRooZCQED377LNKSEi44TmeffZZHT16VL1795abm5seeughtWvXTm5ul1/vslWrVjm+dnNzU1ZWliZNmqTHHntMd911lzIyMtSqVSvNnz/fNQXcbrdr2LBhOnjwoAICAtS+fXu99957kiRPT089//zz2rt3r7y9vXXrrbfqq6++yv8Xng8shokT2P/880+99dZbWrNmjY4cOaK5c+eqc+fOlzxnyZIlGjFihDZv3qxy5crpxRdfVN++fa/4ORMSEhQYGKj4+HgFBARc3wsAAAAwAfczRR8/QwDA9UpLS1NsbKwqVaokLy8vs+OUOA6HQ7Vq1dL999+v//3vf2bHKRCX+h27mnsZU9d8TE5OVv369fXxxx9f0fGxsbG68847ddttt2n9+vV6/PHHNXDgQC1YsKCAkwIAAAAAAKCk2rdvn7744gvt2LFDMTExGjJkiGJjY/Xggw+aHa3QM3XadYcOHdShQ4crPn7cuHGqVKmS3nnnHUnOxTn//vtvvffee2rXzpx28gAA5Ie0TLuW7z6l9Cy72VGQD+qXC1JEoLfZMVDCHY5L1Q8bDuuhVpXztQspAAAlkdVq1eTJk/XUU0/JMAzVrVtXv/32W6FdZ7EwKVJrPi5fvlxt27bNsa9du3Z6/PHHL3pOenq60tPTXV+bsS4AAACXcuB0igZNXa1tRxPNjoJ88tGDDXVXPYqPME9yepbu+3SZDsenyZA0uHUVsyMBAFCklStXTkuXLjU7RpFUpIqPR48eVXh4eI594eHhSkhIUGpqqry9c9/kjxkzRqNGjbpREQEAuCr/7DmloTPW6nRyhkr5eKhKqJ/ZkZAPSvt4mh0BJZyvzV39b6mk137aqv/7eZtC/Wzq0ijK7FgAAKAEKlLFx2vx/PPPa8SIEa6vExISVK5cORMTAQDgNP2ffXrl+83KchiKjgzU570bMVUXQL4ZeGtlHU9M1+d/7tEz325UaT9P3VYjzOxYAACghDG14czVKlOmjI4dO5Zj37FjxxQQEJDnqEdJstlsCggIyLEBAGCmTLtDL86L0YvzNinLYeg/9cvqm8HNKTwCyHfPta+pzg3Kyu4wNHT6Wq0/EGd2JAAAUMIUqeJj8+bNtWjRohz7Fi5cqObNm5uUCACAq3M6OUO9JqzQ9H/2y2KRnmlfQx880EBeHm5mRwNQDFmtFr15X33dWi1EqZl29Z+8SrEnk82OBQAAShBTi49JSUlav3691q9fL0mKjY3V+vXrtX//fknOKdO9e/d2HT948GDt2bNHzzzzjLZt26ZPPvlEX3/9tZ544gkz4gMAcFW2HknQfz76W//sOS0/m7vG926soW2q0oUWQIHydLfq056NFB0ZqNPJGeo9cYWOJ6aZHQsAAJQQphYfV69erYYNG6phw4aSpBEjRqhhw4YaOXKkJOnIkSOuQqQkVapUST/99JMWLlyo+vXr65133tH48ePVrl07U/IDAHClftl0VF0+XaaDZ1JVIdhHc4e20L9rhV/+RADIB342d03s20QVgn104HSq+k5cpcS0TLNjAQCAEsDU4mObNm1kGEaubfLkyZKkyZMna8mSJbnOWbdundLT07V792717dv3hucGAOBKGYahDxft1ODpa5SSYVfLqsH6blhLVQv3NzsagBIm1N+mqf2bKsTPU1uOJGjw9DVKz7KbHQsAgKvWpk0bPf74466vK1asqPfff/+S51gsFs2bN++6nzu/rlOSFKk1HwEAKEpSMrI0fOY6vbtwhySpb4uKmtKvqYJ8PE1OBqCkqhDsq0l9m8rH001Ld53SU99slMNhmB0LAFBCdOrUSe3bt8/zsb/++ksWi0UbN2686uuuWrVKDz300PXGy+GVV15RgwYNcu0/cuSIOnTokK/PdaHJkycrKCioQJ/jRqL4CABAATh4JkX3fbpcP8UckYebRf93b7Re+U8dubvxpxeAuaKjAjWuZyO5Wy36YcNhvfbTVhkGBUgAQMEbMGCAFi5cqIMHD+Z6bNKkSWrcuLHq1at31dcNDQ2Vj49PfkS8rDJlyshms92Q5you+BcQAAD5bNXe07r7o6XaciRBIX6emjnoZj3QtLzZsQDApVX1UL3dtb4kaeLSWH3+5x6TEwEArpthSBnJ5mxX+CbWXXfdpdDQUNdye9mSkpL0zTffaMCAATp16pS6d++uyMhI+fj4KDo6Wl9++eUlr3vhtOudO3eqVatW8vLyUu3atbVw4cJc5zz77LOqXr26fHx8VLlyZb300kvKzHSuhzx58mSNGjVKGzZskMVikcVicWW+cNp1TEyM/vWvf8nb21vBwcF66KGHlJSU5Hq8b9++6ty5s95++21FREQoODhYw4YNcz3Xtdi/f7/uvvtu+fn5KSAgQPfff7+OHTvmenzDhg267bbb5O/vr4CAADVq1EirV6+WJO3bt0+dOnVSqVKl5Ovrqzp16mj+/PnXnOVKuBfo1QEAKGG+WrlfL323SZl2Q7UjAvRFn8aKDPI2OxYA5NK5YaROJKbr9flbNebnbQr1t+nem6LMjgUAuFaZKdLosuY8938PS56+lz3M3d1dvXv31uTJk/XCCy/IYrFIkr755hvZ7XZ1795dSUlJatSokZ599lkFBATop59+Uq9evVSlShU1bdr0ss/hcDh07733Kjw8XCtWrFB8fHyO9SGz+fv7a/LkySpbtqxiYmI0aNAg+fv765lnnlG3bt20adMm/fLLL/rtt98kSYGBgbmukZycrHbt2ql58+ZatWqVjh8/roEDB2r48OE5CqyLFy9WRESEFi9erF27dqlbt25q0KCBBg0adNnXk9fryy48/vHHH8rKytKwYcPUrVs3V9+UHj16qGHDhvr000/l5uam9evXy8PDQ5I0bNgwZWRk6M8//5Svr6+2bNkiPz+/q85xNSg+AgCQDzLtDr3+01ZNXrZXknRndITe6lpPPp78qQVQeA1qVVnHEtI0/u9YPTN7o4L9bGpdPdTsWACAYqx///5666239Mcff6hNmzaSnFOuu3TposDAQAUGBuqpp55yHf/II49owYIF+vrrr6+o+Pjbb79p27ZtWrBggcqWdRZjR48enWudxhdffNH1ecWKFfXUU0/pq6++0jPPPCNvb2/5+fnJ3d1dZcqUuehzzZw5U2lpaZo6dap8fZ3F148++kidOnXSG2+8ofDwcElSqVKl9NFHH8nNzU01a9bUnXfeqUWLFl1T8XHRokWKiYlRbGysypUrJ0maOnWq6tSpo1WrVqlJkybav3+/nn76adWsWVOSVK1aNdf5+/fvV5cuXRQdHS1Jqly58lVnuFr8iwgAgOt0JjlDw2au1bLdpyRJT95eXcP/VdX1Ti4AFGb/7VhLxxPT9f2GwxoyfY2+euhm1YsKMjsWAOBqefg4RyCa9dxXqGbNmmrRooUmTpyoNm3aaNeuXfrrr7/06quvSpLsdrtGjx6tr7/+WocOHVJGRobS09OveE3HrVu3qly5cq7CoyQ1b94813GzZs3Shx9+qN27dyspKUlZWVkKCAi44teR/Vz169d3FR4lqWXLlnI4HNq+fbur+FinTh25ubm5jomIiFBMTMxVPdf5z1muXDlX4VGSateuraCgIG3dulVNmjTRiBEj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rapevbpmzJhR6PG0tDR9/vnnuvfee3Xy5EkNGDBAtWrVkre3t8LDwzVnzpyLvu7/TrveuXOnrrvuOnl6eqpFixZavHjx384ZNWqUmjZtKm9vbzVs2FDPP/+8cnNzJUkzZszQiy++qA0bNsgwDBmGUZD5f6ddb9y4Ud27d5eXl5eqVaum+++/X2lpaQXPDx06VH369NGECRNUo0YNVatWTQ899FDBe13MtGnTNHjwYA0ePFjTpk372/ObN2/WrbfeKj8/P/n6+uraa6/V7t27C56PjY1Vy5YtZbPZVKNGjYJfUu7bt0+GYSghIaHg2DNnzsgwDP3yyy+SpF9++UWGYej7779Xhw4dZLPZ9Ntvv2n37t267bbbFBISoipVqqhjx45asmRJoVzZ2dkaNWqU6tSpI5vNpsaNG2vatGlyOp1q3LixJkyYUOj4hIQEGYahXbt2XfIzAQAAACqicrHhzIgRIy545eK5fwj81V133aW77rqrlFMBACqM3Azp1ZrmvPczRyQPn0se5ubmpujoaM2YMUPPPvtswbrAn3/+uex2uwYMGKC0tDR16NBBo0aNkp+fnxYtWqR77rlHjRo1UmRk5CXfw+Fw6Pbbb1dISIhWr16t5OTkQutDnuPr66sZM2aoZs2a2rhxo+677z75+vrq3//+t/r3769Nmzbphx9+KCjW/P39//Ya6enp6tWrlzp37qz4+HglJSVp+PDhGjFiRKGCddmyZapRo4aWLVumXbt2qX///mrbtq3uu+++C/49du/erVWrVumrr76S0+nU448/rv3796tevXqSpMOHD+u6665T165d9fPPP8vPz08rV64suDrx/fff18iRI/Xaa6/ppptuUnJyslauXHnJz+9/Pf3005owYYIaNmyoqlWr6uDBg7r55pv1yiuvyGazadasWerdu7e2b9+uunXrSsqfsbFq1SpNnjxZbdq00d69e3XixAkZhqGYmBhNnz5dTz75ZMF7TJ8+Xdddd50aN25c7HwAAABARVAuykcAACqDmJgYvfnmm1q+fLm6du0qKb98uuOOO+Tv7y9/f/9CxdTDDz+sH3/8UfPmzStS+bhkyRJt27ZNP/74o2rWzC9jX3311b+t0/jcc88V/Ll+/fp68sknNXfuXP373/+Wl5eXqlSpIjc3twtu5iZJs2fPVlZWlmbNmiUfn/zydcqUKerdu7def/31ghkMVatW1ZQpU2S1WtW8eXPdcsstWrp06UXLx9jYWN10002qWrWqJKlXr16aPn26xo4dK0l699135e/vr7lz58rd3V2S1LRp04LzX375ZT3xxBN69NFHCx7r2LHjJT+//zVu3Dj17Nmz4H5gYKDatGlTcP+ll17S/PnztXDhQo0YMUI7duzQvHnztHjxYkVFRUmSGjZsWHD80KFDNWbMGMXFxSkyMlK5ubmaPXv2366GBAAAAFwJ5SMAoOJz986/AtGs9y6i5s2b6+qrr1ZsbKy6du2qXbt2acWKFRo3bpwkyW6369VXX9W8efN0+PBh5eTkKDs7u8hrOm7dulV16tQpKB4lnXdDts8++0yTJ0/W7t27lZaWpry8PPn5+RX573Huvdq0aVNQPEpSly5d5HA4tH379oLysWXLlrJa/7vbXo0aNbRx48YLvq7dbtfMmTP19ttvFzw2ePBgPfnkkxozZowsFosSEhJ07bXXFhSPf5WUlKQjR46oR48exfr7nE9ERESh+2lpaRo7dqwWLVqko0ePKi8vT5mZmTpw4ICk/CnUVqtV119//Xlfr2bNmrrlllsUGxuryMhIffPNN8rOzmY2BwAAAFya6Ws+AgBwxQwjf+qzGbez06eL6t5779WXX36p1NRUTZ8+XY0aNSooq9588029/fbbGjVqlJYtW6aEhAT16tVLOTk5JfZRrVq1SoMGDdLNN9+sb7/9VuvXr9ezzz5bou/xV/9bEBqGIYfDccHjf/zxRx0+fFj9+/eXm5ub3NzcdPfdd2v//v1aunSpJMnLy+uC51/sOUmyWPKHPs6/rNV5oTUo/1qsStKTTz6p+fPn69VXX9WKFSuUkJCg8PDwgs/uUu8tScOHD9fcuXOVmZmp6dOnq3///mW2YRAAAABgBspHAADKUL9+/WSxWDR79mzNmjVLMTExBes/rly5UrfddpsGDx6sNm3aqGHDhtqxY0eRXzssLEwHDx4stFHbH3/8UeiY33//XfXq1dOzzz6riIgINWnSRPv37y90jIeHh+x2+yXfa8OGDUpPTy94bOXKlbJYLGrWrFmRM/+vadOm6e6771ZCQkKh2913312w8Uzr1q21YsWK85aGvr6+ql+/fkFR+b+qV68uSYU+o79uPnMxK1eu1NChQ9W3b1+Fh4crNDRU+/btK3g+PDxcDodDy5cvv+Br3HzzzfLx8dH777+vH374QTExMUV6bwAAAKCionwEAKAMValSRf3799fo0aN19OhRDR06tOC5Jk2aaPHixfr999+1detW/fOf/9SxY8eK/NpRUVFq2rSphgwZog0bNmjFihV69tlnCx3TpEkTHThwQHPnztXu3bs1efJkzZ8/v9Ax9evX1969e5WQkKATJ04oOzv7b+81aNAgeXp6asiQIdq0aZOWLVumhx9+WPfcc0/BlOviOn78uL755hsNGTJErVq1KnSLjo7WggULdOrUKY0YMUIpKSm6++67tWbNGu3cuVMff/yxtm/fLkkaO3asJk6cqMmTJ2vnzp1at26d3nnnHUn5VydeddVVeu2117R161YtX7680BqYF9OkSRN99dVXSkhI0IYNGzRw4MBCV3HWr19fQ4YMUUxMjBYsWKC9e/fql19+0bx58wqOsVqtGjp0qEaPHq0mTZqcd1o8AAAA4EooHwEAKGP33nuvTp8+rV69ehVan/G5555T+/bt1atXL3Xt2lWhoaHq06dPkV/XYrFo/vz5yszMVGRkpIYPH65XXnml0DH/+Mc/9Pjjj2vEiBFq27atfv/9dz3//POFjrnjjjt04403qlu3bqpevbrmzJnzt/fy9vbWjz/+qFOnTqljx46688471aNHD02ZMqV4H8ZfnNu85nzrNfbo0UNeXl765JNPVK1aNf38889KS0vT9ddfrw4dOmjq1KkFU7yHDBmiSZMm6b333lPLli116623aufOnQWvFRsbq7y8PHXo0EGPPfaYXn755SLle+utt1S1alVdffXV6t27t3r16qX27dsXOub999/XnXfeqQcffFDNmzfXfffdV+jqUCn/+8/JydGwYcOK+xEBAAAAFY7h/OuiR5VASkqK/P39lZycXOzF9QEA5svKytLevXvVoEEDeXp6mh0HKLYVK1aoR48eOnjw4EWvEr3YzzrjmYqP7xAAAFRkxRnLsNs1AABAGcjOztbx48c1duxY3XXXXZc9PR0AAACoSJh2DQAAUAbmzJmjevXq6cyZM3rjjTfMjgMAAACUCcpHAACAMjB06FDZ7XatXbtWtWrVMjsOAAAAUCYoHwEAAAAAAACUCspHAECFVMn2S0MlxM84AAAAXAHlIwCgQnF3d5ckZWRkmJwEKF3nfsbP/cwDAAAAFRG7XQMAKhSr1aqAgAAl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UkJCQsFty5YtBWvsXCkvL68iHffXKSuGYUjKX/tHksaOHavNmzfrlltu0c8//6wWLVpo/vz5JZIPAAAA5mJMCqAyoHwEUCm1aNFCNptNBw4cUOPGjQvd6tSpU3DcH3/8UfDn06dPa8eOHQoLC5MkhYWFaeXKlYVed+XKlWratKmsVqvCw8PlcDgKrddzOZo2barHH39cP/30k26//XZNnz79il4PAAAA5QNjUgCVgZvZAQDADL6+vnryySf1+OOPy+Fw6JprrlFycrJWrlwpPz8/1atXT5I0btw4VatWTSEhIXr22WcVFBSkPn36SJKeeOIJdezYUS+99JL69++vVatWacqUKXrvvfckSfXr19eQIUMUExOjyZMnq02bNtq/f7+SkpLUr1+/S2bMzMzUU089pTvvvFMNGjTQoUOHFB8frzvuuKPUPhcAAACUHcakACoDykcAldZLL72k6tWra/z48dqzZ48CAgLUvn17PfPMMwVTTF577TU9+uij2rlzp9q2batvvvlGHh4ekqT27dtr3rx5GjNmjF566SXVqFFD48aN09ChQwve4/3339czzzyjBx98UCdPnlTdunX1zDPPFCmf1WrVyZMnFR0drWPHjikoKEi33367XnzxxRL/LAAAAGAOxqQAXB27XQPAeZzb9e/06dMKCAgwOw4AAAAqIcakAFwBaz4CAAAAAAAAKBWUjwAAAAAAAABKBdOuAQAAAAAAAJQKrnwEAAAAAAAAUCooHwEAAAAAAACUCspHAAAAAAAAAKWC8hEAAAAAAABAqaB8BAAAAAAAAFAqKB8BAAAAAAAAlArKRwAAAAAAAAClgvIRAAAAAAAAQKn4f7sfrrR7tSQ4AAAAAElFTkSuQmCC",
            "text/plain": [
              "<Figure size 1600x800 with 2 Axes>"
            ]
          },
          "metadata": {},
          "output_type": "display_data"
        }
      ],
      "source": [
        "# Learning curves \n",
        "\n",
        "acc = history1.history['accuracy']\n",
        "val_acc = history1.history['val_accuracy']\n",
        "loss=history1.history['loss']\n",
        "val_loss=history1.history['val_loss']\n",
        "\n",
        "plt.figure(figsize=(16,8))\n",
        "plt.subplot(1, 2, 1)\n",
        "plt.plot(acc, label='Training Accuracy')\n",
        "plt.plot(val_acc, label='Validation Accuracy')\n",
        "plt.legend(loc='lower right')\n",
        "plt.title('Training and Validation Accuracy')\n",
        "plt.xlabel(\"epochs\")\n",
        "plt.ylabel(\"accuracy\")\n",
        "\n",
        "plt.subplot(1, 2, 2)\n",
        "plt.plot(loss, label='Training Loss')\n",
        "plt.plot(val_loss, label='Validation Loss')\n",
        "plt.legend(loc='upper right')\n",
        "plt.title('Training and Validation Loss')\n",
        "plt.xlabel(\"epochs\")\n",
        "plt.ylabel(\"loss\")\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "mdIDkqyABJbr"
      },
      "source": [
        "## CNN"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 63,
      "metadata": {
        "id": "0sR_Z8kDX8VD"
      },
      "outputs": [],
      "source": [
        "def define_model2(vocab_size, max_length):\n",
        "    model2 = Sequential()\n",
        "    model2.add(Embedding(vocab_size,300, input_length=max_length))\n",
        "    model2.add(Conv1D(filters=32, kernel_size=2, activation='relu'))\n",
        "    model2.add(MaxPooling1D(pool_size = 4))\n",
        "    model2.add(Flatten())\n",
        "    model2.add(Dense(32, activation='relu'))\n",
        "    model2.add(Dense(10, activation='softmax'))\n",
        "    \n",
        "    model2.compile(loss = 'categorical_crossentropy',optimizer = 'adam',metrics = ['accuracy'])\n",
        "    \n",
        "    # summarize defined model\n",
        "    model2.summary()\n",
        "    return model2"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 64,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "n1ePmE7PX8R0",
        "outputId": "94070aba-3771-4325-e72a-27f8f9475f7d"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Model: \"sequential_1\"\n",
            "_________________________________________________________________\n",
            " Layer (type)                Output Shape              Param #   \n",
            "=================================================================\n",
            " embedding_1 (Embedding)     (None, 10, 300)           19800     \n",
            "                                                                 \n",
            " conv1d (Conv1D)             (None, 9, 32)             19232     \n",
            "                                                                 \n",
            " max_pooling1d (MaxPooling1  (None, 2, 32)             0         \n",
            " D)                                                              \n",
            "                                                                 \n",
            " flatten (Flatten)           (None, 64)                0         \n",
            "                                                                 \n",
            " dense_1 (Dense)             (None, 32)                2080      \n",
            "                                                                 \n",
            " dense_2 (Dense)             (None, 10)                330       \n",
            "                                                                 \n",
            "=================================================================\n",
            "Total params: 41442 (161.88 KB)\n",
            "Trainable params: 41442 (161.88 KB)\n",
            "Non-trainable params: 0 (0.00 Byte)\n",
            "_________________________________________________________________\n"
          ]
        }
      ],
      "source": [
        "model2 = define_model2(vocab_size, max_length)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 65,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "CnC_x02JX8Pd",
        "outputId": "93ae2b41-a447-4a9d-fa8b-952ceea4b9f6"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Epoch 1/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.3108 - accuracy: 0.0833\n",
            "Epoch 1: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 364ms/step - loss: 2.3108 - accuracy: 0.0833 - val_loss: 2.3017 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 2/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.2664 - accuracy: 0.4167\n",
            "Epoch 2: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 18ms/step - loss: 2.2664 - accuracy: 0.4167 - val_loss: 2.2972 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 3/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.2331 - accuracy: 0.4167\n",
            "Epoch 3: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 18ms/step - loss: 2.2331 - accuracy: 0.4167 - val_loss: 2.2930 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 4/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.2032 - accuracy: 0.5000\n",
            "Epoch 4: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 18ms/step - loss: 2.2032 - accuracy: 0.5000 - val_loss: 2.2887 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 5/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.1736 - accuracy: 0.5000\n",
            "Epoch 5: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 18ms/step - loss: 2.1736 - accuracy: 0.5000 - val_loss: 2.2847 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 6/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.1425 - accuracy: 0.5833\n",
            "Epoch 6: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 18ms/step - loss: 2.1425 - accuracy: 0.5833 - val_loss: 2.2814 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 7/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.1111 - accuracy: 0.6667\n",
            "Epoch 7: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 18ms/step - loss: 2.1111 - accuracy: 0.6667 - val_loss: 2.2776 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 8/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.0779 - accuracy: 0.7500\n",
            "Epoch 8: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 18ms/step - loss: 2.0779 - accuracy: 0.7500 - val_loss: 2.2741 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 9/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.0435 - accuracy: 0.7500\n",
            "Epoch 9: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 18ms/step - loss: 2.0435 - accuracy: 0.7500 - val_loss: 2.2700 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 10/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 2.0075 - accuracy: 0.7500\n",
            "Epoch 10: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 18ms/step - loss: 2.0075 - accuracy: 0.7500 - val_loss: 2.2647 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 11/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 1.9703 - accuracy: 0.7500\n",
            "Epoch 11: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 17ms/step - loss: 1.9703 - accuracy: 0.7500 - val_loss: 2.2597 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 12/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 1.9321 - accuracy: 0.7500\n",
            "Epoch 12: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 18ms/step - loss: 1.9321 - accuracy: 0.7500 - val_loss: 2.2550 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 13/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 1.8929 - accuracy: 0.7500\n",
            "Epoch 13: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 19ms/step - loss: 1.8929 - accuracy: 0.7500 - val_loss: 2.2503 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 14/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 1.8526 - accuracy: 0.7500\n",
            "Epoch 14: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 17ms/step - loss: 1.8526 - accuracy: 0.7500 - val_loss: 2.2451 - val_accuracy: 0.2000 - lr: 0.0010\n",
            "Epoch 15/15\n",
            "1/1 [==============================] - ETA: 0s - loss: 1.8112 - accuracy: 0.7500\n",
            "Epoch 15: val_loss did not improve from 2.10980\n",
            "1/1 [==============================] - 0s 18ms/step - loss: 1.8112 - accuracy: 0.7500 - val_loss: 2.2400 - val_accuracy: 0.2000 - lr: 0.0010\n"
          ]
        }
      ],
      "source": [
        "history = model2.fit(X_train, y_train, epochs=15, verbose=1,validation_data=(X_test,y_test),callbacks=callbacks)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 66,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 513
        },
        "id": "SMNZHhfqYEQ9",
        "outputId": "0c81da43-c58a-419d-b477-9afb5cb5c262"
      },
      "outputs": [
        {
          "data": {
            "image/png": "iVBORw0KGgoAAAANSUhEUgAABR8AAAK9CAYAAACtshu3AAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8WgzjOAAAACXBIWXMAAA9hAAAPYQGoP6dpAADmm0lEQVR4nOzdd3gU5eL28Xt303sFAgkEQu+9KUWlq0c8qIhIk6IIWBALr0dU9CdHQUXRI0hVqYqAnSqgIk16r4HQIYF0UnfePxYCIaGTTMr3c11zJTs7s3vvEmBy7zPPWAzDMAQAAAAAAAAAd5jV7AAAAAAAAAAAiibKRwAAAAAAAAB5gvIRAAAAAAAAQJ6gfAQAAAAAAACQJygfAQAAAAAAAOQJykcAAAAAAAAAeYLyEQAAAAAAAECeoHwEAAAAAAAAkCcoHwEAAAAAAADkCcpHoBDo3bu3wsPDb2nft956SxaL5c4GKmAOHToki8WiadOm5ftzWywWvfXWW1m3p02bJovFokOHDl133/DwcPXu3fuO5rmdnxUAAID8wvHttXF8ewnHt0DhR/kI3AaLxXJDy4oVK8yOWuw999xzslgs2r9//1W3ef3112WxWLR169Z8THbzjh8/rrfeekubN282O0qudu3aJYvFIjc3N8XGxpodBwAA3ASObwsPjm/z1sUCeMyYMWZHAQo9J7MDAIXZN998k+32119/rSVLluRYX61atdt6nokTJ8put9/Svv/5z3/02muv3dbzFwXdu3fXuHHjNHPmTI0YMSLXbWbNmqVatWqpdu3at/w8PXr00OOPPy5XV9dbfozrOX78uN5++22Fh4erbt262e67nZ+VO2X69OkqVaqUzp07p7lz56pfv36m5gEAADeO49vCg+NbAIUF5SNwG5588slst9esWaMlS5bkWH+l5ORkeXh43PDzODs731I+SXJycpKTE3/VmzRpoooVK2rWrFm5HpytXr1akZGR+u9//3tbz2Oz2WSz2W7rMW7H7fys3AmGYWjmzJl64oknFBkZqRkzZhTY8jEpKUmenp5mxwAAoEDh+Lbw4PgWQGHBaddAHmvdurVq1qypDRs2qGXLlvLw8ND/+3//T5L0ww8/6P7771fp0qXl6uqqiIgIvfPOO8rMzMz2GFfOc3L5KQBffvmlIiIi5OrqqkaNGmn9+vXZ9s1tThyLxaLBgwdrwYIFqlmzplxdXVWjRg0tXLgwR/4VK1aoYcOGcnNzU0REhCZMmHDD8+z8+eefevTRR1W2bFm5uroqLCxML774os6fP5/j9Xl5eenYsWPq3LmzvLy8FBwcrGHDhuV4L2JjY9W7d2/5+vrKz89PvXr1uuFTe7t3767du3dr48aNOe6bOXOmLBaLunXrprS0NI0YMUINGjSQr6+vPD091aJFCy1fvvy6z5HbnDiGYejdd99VaGioPDw8dM8992jHjh059j179qyGDRumWrVqycvLSz4+PurYsaO2bNmStc2KFSvUqFEjSVKfPn2yTn26OB9QbnPiJCUl6aWXXlJYWJhcXV1VpUoVjRkzRoZhZNvuZn4urmbVqlU6dOiQHn/8cT3++OP6448/dPTo0Rzb2e12ffLJJ6pVq5bc3NwUHBysDh066J9//sm23fTp09W4cWN5eHjI399fLVu21OLFi7NlvnxOoouunG/o4p/LypUr9eyzz6pEiRIKDQ2VJB0+fFjPPvusqlSpInd3dwUGBurRRx/NdV6j2NhYvfjiiwoPD5erq6tCQ0PVs2dPRUdHKzExUZ6ennr++edz7Hf06FHZbDaNGjXqBt9JAAAKLo5vOb4tTse313P69Gn17dtXJUuWlJubm+rUqaOvvvoqx3azZ89WgwYN5O3tLR8fH9WqVUuffPJJ1v3p6el6++23ValSJbm5uSkwMFB33323lixZcseyAmbh4yIgH8TExKhjx456/PHH9eSTT6pkyZKSHP+Re3l5aejQofLy8tLvv/+uESNGKD4+XqNHj77u486cOVMJCQl6+umnZbFY9MEHH+jf//63Dh48eN1PCP/66y/NmzdPzz77rLy9vfXpp5+qS5cuioqKUmBgoCRp06ZN6tChg0JCQvT2228rMzNTI0eOVHBw8A297u+++07JyckaOHCgAgMDtW7dOo0bN05Hjx7Vd999l23bzMxMtW/fXk2aNNGYMWO0dOlSffjhh4qIiNDAgQMlOQ5yHnroIf3111965plnVK1aNc2fP1+9evW6oTzdu3fX22+/rZkzZ6p+/frZnvvbb79VixYtVLZsWUVHR2vSpEnq1q2b+vfvr4SEBE2ePFnt27fXunXrcpwKcj0jRozQu+++q06dOqlTp07auHGj2rVrp7S0tGzbHTx4UAsWLNCjjz6q8uXL69SpU5ow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eirHvJMjR45UbGysKleurFq1aunll1/W1q1bbzsjUBBQPgL54PJPSC+KjY1Vq1attGXLFo0cOVI//fSTlixZkjUHiN1uv+7jXu2qc8YVEy3f6X1vRGZmptq2batffvlFr776qhYsWKAlS5ZkTRx95evLryvolShRQm3bttX333+v9PR0/fTTT0pISMg2F9/06dPVu3dvRUREaPLkyVq4cKGWLFmie++994b+XG7Ve++9p6FDh6ply5aaPn26Fi1apCVLlqhGjRp5+ryXu9Wfi/j4eP3000+KjIxUpUqVspbq1asrOTlZM2fOvGM/WzfiyoncL8rt7+KQIUP0f//3f3rsscf07bffavHixVqyZIkCAwNv6X3v2bOnEhMTtWDBgqyrfz/wwAPy9fW96ccCAKCg4viW49sbUZiPb++kEiVKaPPmzfrxxx+z5qvs2LFjtrk9W7ZsqQMHDmjKlCmqWbOmJk2apPr162vSpEn5lhPIK1xwBjDJihUrFBMTo3nz5qlly5ZZ6yMjI01MdUmJEiXk5uam/fv357gvt3VX2rZtm/bu3auvvvpKPXv2zFp/O1drK1eunJYtW6bExMRsnw7v2bPnph6ne/fuWrhwoX777TfNnDlTPj4+evDBB7Punzt3ripUqKB58+ZlO5Ukt9OEbySzJO3bt08VKlTIWn/mzJkcn7bOnTtX99xzjyZPnpxtfWxsrIKCgrJu38xpx+XKldPSpUuVkJCQ7dPhi6c9Xcx3u+bNm6eUlBR98cUX2bJKjj+f//znP1q1apXuvvtuRUREaNGiRTp79uxVRz9GRETIbrdr586d15wA3d/fP8fVINPS0nTixIkbzj537lz16tVLH374Yda6lJSUHI8bERGh7du3X/fxatasqXr16mnGjBkKDQ1VVFSUxo0bd8N5AAAorDi+vXkc3zoUxOPbG82ydetW2e32bKMfc8vi4uKiBx98UA8++KDsdrueffZZTZgwQW+88UbWyNuAgAD16dNHffr0UWJiolq2bKm33npL/fr1y7fXBOQFRj4CJrn4Cdzln7ilpaXpf//7n1mRsrHZbGrTpo0WLFig48ePZ63fv39/jnlUrra/lP31GYahTz755JYzderUSRkZGfriiy+y1mVmZt50sdO5c2d5eHjof//7n3777Tf9+9//lpub2zWzr127VqtXr77pzG3atJGz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99/XjBkzNHXqVFWrVk2ffPKJFixYoHvuueeWX2vv3r21b98+/fjjj/Lx8dGrr76qTp06aefOnXJ2dtagQYOUlpamP/74Q56entq5c2fW6NA33nhDO3fu1G+//aagoCDt379f58+fv+UseYnyEQAAAAAAAAXCyJEj1bZt26zbAQEBqlOnTtbtd955R/Pnz9ePP/6owYMHX/VxevfurW7dukmS3nvvPX366adat26dOnTokOv26enpGj9+vCIiIiRJgwcP1siRI7PuHzdunIYPH66HH35YkvTZZ59ljUK8FRdLx1WrVql58+aSpBkzZigsLEwLFizQo48+qqioKHXp0kW1atWSJFWoUCFr/6ioKNWrV08NGzaU5Bj9WVBRPgIAAAAAABRy7s427RzZ3rTnvlMulmkXJSYm6q233tIvv/yiEydOKCMjQ+fPn1dUVNQ1H6d27dpZ33t6esrHx0enT5++6vYeHh5ZxaMkhYSEZG0fFxenU6dOqXHjxln322w2NWjQQHa7/aZe30W7du2Sk5OTmjRpkrUuMDBQVapU0a5duyRJzz33nAYOHKjFixerTZs26tKlS9brGjhwoLp06aKNGzeqXbt26ty5c1aJWdAw5yMAAAAAAEAhZ7FY5OHiZMpisVju2Ovw9PTMdnvYsGGaP3++3nvvPf3555/avHmzatWqpbS0tGs+jrOzc47351pFYW7b3+hclnmlX79+OnjwoHr06KFt27apYcOGGjdunCSpY8eOOnz4sF588UUdP35c9913n4YNG2Zq3quhfAQAAAAAAECBtGrVKvXu3VsPP/ywatWqpVKlSunQoUP5msHX11clS5bU+vXrs9ZlZmZq48aNt/yY1apVU0ZGhtauXZu1LiYmRnv27FH16tWz1oWFhemZZ57RvHnz9NJLL2nixIlZ9wUHB6tXr16aPn26xo4dqy+//PKW8+QlTrsGAAAAAABAgVSpUiXNmzdPDz74oCwWi954441bPtX5dgwZMkSjRo1SxYoVVbVqVY0bN07nzp27oVGf27Ztk7e3d9Zti8WiOnXq6KGHHlL//v01YcIEeXt767XXXlOZMmX00EMPSZJeeOEFdezYUZUrV9a5c+e0fPlyVatWTZI0YsQINWjQQDVq1FBqaqp+/vnnrPsKGspHAAAAAAAAFEgfffSRnnrqKTVv3lxBQUF69dVXFR8f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fAQAAAAAlJAqZf01p29jBft6aFPSGfWbuV6ZORajYwEwwDWVj+vWrdPatWsvOr527VqtX7/+qt5r0KBBmjJlimbOnKnt27frySefVHp6unr16iVJ6t69u31DGm9vb9WpUyffIzg4WAEBAapTp84lN8EpzbJzrTqceqF8ZM1HAAAAAEBJqhERqJm9Gsvfy12r957UU59uVI7FanQsACXsmsrH/v37Kzk5+aLjhw4dUv/+/a/qvTp27KixY8dq6NChql+/vhITE7VkyRL7JjRJSUlKSUm5lpil3uEz52WzST4eZpXxp5gFAAAAAJSs2KhgTe0RL28PN/2445gGf/G7rFab0bEAlCCTzWa76n/r/f399fvvv6tKlSr5ju/bt0/16tXT2bNniyxgUUtLS1NQUJBSU1MVGBhodJxi9fOu4+o+LUE3hPvr/567ulviAQCA4ypN4xlXxZ8hgNLmxx1H1W/WBlmsNj12SxW90qam0ZEAXIerGctc08xHLy+vizaJkaSUlBS5u7OArKNIPs1O1wAAAAAA491eI1yjH6onSfr45736+Oc9BicCUFKuqXy86667NGTIEKWmptqPnTlzRq+88oruvPPOIguH65O303UU6z0CAAAAAAz2cFxFDbmnhiRpxHc79NXGgwYnAlASrmma4tixY3XLLbeoUqVKatCggSQpMTFR4eHhmj17dpEGxLU7eOrCZjOUjwAAAAAAR/DYLVV0/GyWPvl1n1764neF+HnqthvLGR0LQDG6ppmPFSpU0O+//64xY8aoVq1aiouL0wcffKAtW7YoKiqqqDPiGv1927WPwUkAAAAAAJBMJpNeaVNT7eqXV67VpqfmbNTGpNNGxwJQjK55gUY/Pz+1aNFC0dHRys7OliR9//33kqT777+/aNLhuuTddh0dxsxHAAAAAIBjcHMzaczDsTqVkaOfdx1X7xnr9MUTTVWtXIDR0QAUg2sqH/fu3av27dtry5YtMplMstlsMplM9uctFkuRBcS1ScvM0ZmMHElsOAMAAAAAcCye7m6a1KWhHv1krTYnn1H3qQn68qlmigzizj3A1VzTbdcDBw5U5cqVdezYMfn6+mrr1q366aefFB8fr5UrVxZxRFyL5L9mPYb5ecrPix3IAQAAAACOxc/LXdN7NlKVsn46nJqpHtMSdCYj2+hYAIrYNZWPq1ev1vDhw1Wm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kEwmk/3rHTt2KCAgQN9//73i4uLk5eWlX3/9VXv27NEDDzyg8PBw+fv7q1GjRlq2bFm+9/33bdcmk0mffPKJ2rdvL19fX1WvXl2LFi2yP//v265nzJih4OBg/fDDD6pZs6b8/f119913KyUlxf6a3NxcPfPMMwoODlZYWJgGDx6sHj16qF27dgV+31OnTtWjjz6qbt26XfK/7wcPHlTnzp0VGhoqPz8/xcfHa+3atfbnv/nmGzVq1Eje3t4qU6aM2rdvn+97/frrr/O9X3BwsGbMmCFJ2r9/v0wmkxYsWKBbb71V3t7e+vTTT3Xy5El17txZFSpUkK+vr+rWrat58+blex+r1aoxY8aoWrVq8vLyUnR0tN555x1J0u23364BAwbkO//48ePy9PTU8uXLC7wmAAAAQGE81bKa7qoVrmyLVU/O2aAT57KMjnRN3I364OzsbG3YsEFDhgyxH3Nzc1OrVq20evXqIvucrKwsZWX9/YeTlpZWZO9dkH+u98iOlQBQfM7nWFRr6A+GfPYfw1vL17No/nP68ssva+zYsapSpYpCQkKUnJysNm3a6J133pGXl5dmzZqltm3baufOnYqOjr7s+7z55psaM2aM3n33XX344Yfq0qWLDhw4oNDQ0Euen5GRobFjx2r27Nlyc3NT165d9cILL+jTTz+VJI0ePVqffvqppk+frpo1a+qDDz7Q119/rdtuu+2K38/Zs2f1+eefa+3atapRo4ZSU1P1yy+/6Oabb5YknTt3TrfeeqsqVKigRYsWKSIiQhs3bpTVapUkLV68WO3bt9err76qWbNmKTs7W9999901Xddx48apQYMG8vb2VmZmpuLi4jR48GAFBgZq8eLF6tatm6pWrarGjRtLkoYMGaIpU6boP//5j1q0aKGUlBTt2LFDktS3b18NGDBA48aNs/8ydM6cOapQoYJuv/32q84HAAAAXIqbm0njOsTqgQmrtPdEup6eu0mz+zSWu9nwVRSvimHl44kTJ2SxWBQeHp7veHh4uH1wXxRGjhypN998s8je72qw0zUA4GoMHz5cd955p/3r0NBQxcbG2r9+6623tHDhQi1atOiimXf/1LNnT3Xu3FmSNGLECI0fP14JCQm6++67L3l+Tk6OJk+erKpVq0qSBgwYoOHDh9uf//DDDzVkyBD7rMMJEyYUqgScP3++qlevrtq1a0uSOnXqpKlTp9rLx7lz5+r48eNat26dvRitVq2a/fXvvPOOOnXqlO+/4/+8HoX17LPP6sEHH8x37J+3uT/99NP64Ycf9Nlnn6lx48Y6e/asPvjgA02YMEE9evSQJFWtWlUtWrSQJD344IMaMGCA/ve//6lDhw6SLswg7dmzJ79sBAAAQJEK8PbQR93i1G7iKq3ee1JjftipV9rUNDrWVTGsfCwpQ4YM0aBBg+xfp6WlKSoqqkQ+O+nUhc1mWO8RAIqXj4dZfwxvbdhnF5X4+Ph8X587d07Dhg3T4sWLlZKSotzcXJ0/f15JSVdecLpevXr2f/bz81NgYOBl11OWJF9fX3vxKEmRkZH281NTU3X06FH7jEBJMpvNiouLs89QvJxp06apa9eu9q+7du2qW2+9VR9++KECAgKUmJioBg0aXHZGZmJiovr163fFzyiMf19Xi8WiESNG6LPPPtOhQ4eUnZ2trKws+9qZ27dvV1ZWlu64445Lvp+3t7f9NvIOHTpo48aN2rp1a77b2wEAAICiUj08QGMfidWTn27Uxz/vVb2KQbqvXnmjYxWaYeVjmTJlZDabdfTo0XzHjx49WqSbyXh5eRm2PmTyaWY+AkBJMJlMRXbrs5H8/Pzyff3CCy9o6dKlGjt2rKpVqyYfHx89/PDDys7OvuL7eHjkX2fYZDJdsSi81PmFXcvycv744w+tWbNGCQkJGjx4sP24xWLR/Pnz1a9fP/n4XPmXcwU9f6mcl9pQ5t/X9d1339UHH3yg999/X3Xr1pWfn5+effZZ+3Ut6HOlC7de169fXwcPHtT06dN1++23q1KlSgW+DgAAALgW99SN1BO3VtXkn/bopS9+V/VyAboxIsDoWIVi2E3inp6eiouLy7cwu9Vq1fLly9W0aVOjYhWpvNuuK1I+AgCuwapVq9SzZ0+1b99edevWVUREhPbv31+iGYKCghQeHq5169bZj1ksFm3cuPGKr5s6dapuueUWbd68WYmJifbHoEGDNHXqVEkXZmgmJibq1KlTl3yPevXqXXEDl7Jly+bbGGf37t3KyMgo8HtatWqVHnjgAXXt2lWxsbGqUqWKdu3aZX++evXq8vHxueJn161bV/Hx8ZoyZYrmzp2r3r17F/i5AAAAwPV44a4b1KJaGWVkW/T47PVKPX/xL94dkaErVA4aNEhTpkzRzJkztX37dj355JNKT09Xr169JEndu3fPtyFNdna2/X9esrOzdejQISUmJurPP/806lu4LJvNxpqPAIDrUr16dX311VdKTEzU5s2b9eijjxZ4q3NxePrppzVy5Ej973//086dOzVw4ECdPn36susb5uTkaPbs2ercubPq1KmT79G3b1+tXbtW27ZtU+fOnRUREaF27dpp1apV2rt3r7788kv7xnNvvPGG5s2bpzfeeEPbt2/Xli1bNHr0aPvn3H777ZowYYI2bdqk9evX64knnrhoFuelVK9eXUuXLtVvv/2m7du36/HHH893J4a3t7cGDx6sl156SbNmzdKePXu0Zs0ae2map2/fvho1apRsNlu+XbgBAACA4uBudtP4zg1UIdhH+09maNCCRFmt13fHUkkwtHzs2LGjxo4dq6FDh6p+/fpKTEzUkiVL7JvQJCUl5ZvRcPjwYTVo0EANGjRQSkqKxo4dqwYNGqhv375GfQuXdSo9W+nZFklShWDWfAQAXL333ntPISEhatasmdq2bavWrVurYcOGJZ5j8ODB6ty5s7p3766mTZvK399frVu3lre39yXPX7RokU6ePHnJQq5mzZqqWbOmpk6dKk9PT/3f//2fypUrpzZt2qhu3boaNWqUzOYL62i2bNlSn3/+uRYtWqT69evr9ttvV0JCgv29xo0bp6ioKN1888169NFH9cILL9jXbbyS1157TQ0bNlTr1q3VsmVLewH6T6+//rqef/55DR06VDVr1lTHjh0vWjezc+fOcnd3V+fOnS97LQAAAICiFOrnqcld4+Tp7qblO47pwx8db0Lev5ls17uok5NJS0tTUFCQUlNTFRgYWGyfk5h8Ru0mrlJ4oJfWvtKq2D4HAEqbzMxM7du3T5UrV6bwMYjValXNmjXVoUMHvfXWW0bHMcz+/ftVtWpVrVu3rlhK4Sv9rJfUeAbFhz9DAABwPT5fn6wXv/hdJpM0tUe8bq8RXqKffzVjGUNnProybrkGALiKAwcOaMqUKdq1a5e2bNmiJ598Uvv27dOjjz5qdDRD5OTk6MiRI3rttdd00003GTIbFQAAAKXbI/FR6nZTJdls0rPzE7X/RLrRkS6L8rGYJP1VPkaFUD4CAJybm5ubZsyYoUaNGql58+basmWLli1bppo1axodzRCrVq1SZGSk1q1bp8mTJxsdBwAAAKXU6/fVUsPoYKVl5uqJORuUkZ1rdKRLcjc6gKs6ePqv8pGZjwAAJxcVFaVVq1YZHcNhtGzZUqVs1RoAAAA4IE93N03qGqd7x/+qHUfO6uUvt+iDTvUvuzGkUZj5WEzsMx8pHwEAAAAAAFAMwgO99d8uDeXuZtKizYc1bdV+oyNdhPKxmCSfOi+JNR8BAAAAAABQfBpXDtVr915YEmnEd9u1es9JgxPlR/lYDHItVh06c6F8jAr1MTgNAAAAAAAAXFmPZjFq36CCLFabBszdqJTU80ZHsqN8LAYpqZmyWG3yNLspPMDb6DgAAAAAAABwYSaTSSPa11XNyECdTM/WE3M2KtdiNTqWJMrHYpFjserm6mV0U9Uwubk51iKfAAAAAAAAcD0+nmZ91DVO5QK81KVxtNzNjlH7sdt1MahS1l+z+zQxOgYAAAAAAABKkegwX/380m3y9jAbHcXOMSpQAABQKC1bttSzzz5r/zomJkbvv//+FV9jMpn09ddfX/dnF9X7AAAAACg+jlQ8SpSPAACUiLZt2+ruu+++5HO//PKLTCaTfv/996t+33Xr1umxxx673nj5DBs2TPXr17/oeEpKiu65554i/azLOX/+vEJDQ1WmTBllZWWVyGcCAAAAKHqUjwAAlIA+ffpo6dKlOnjw4EXPTZ8+XfHx8apXr95Vv2/ZsmXl6+tbFBELFBERIS8vrxL5rC+//FK1a9dWjRo1DJ9tabPZlJuba2gGAAAAwFlRPgIAnJ/NJmWnG/Ow2QoV8b777lPZsmU1Y8aMfMfPnTunzz//XH369NHJkyfVuXNnVahQQb6+vqpbt67mzZt3xff9923Xu3fv1i233CJvb2/VqlVLS5cuveg1gwcP1g033CBfX19VqVJFr7/+unJyciRJM2bM0JtvvqnNmzfLZDLJZDLZM//7tustW7bo9ttvl4+Pj8LCwvTYY4/p3Llz9ud79uypdu3aaezYsYqMjFRYWJj69+9v/6wrmTp1qrp27aquXbtq6tSpFz2/bds23XfffQoMDFRAQIBuvvlm7dmzx/78tGnTVLt2bXl5eSkyMlIDBgyQJO3fv18mk0mJiYn2c8+cOSOTyaSVK1dKklauXCmTyaTvv/9ecXFx8vLy0q+//qo9e/bogQceUHh4uPz9/dWoUSMtW7YsX66srCwNHjxYUVFR8vLyUrVq1TR16lTZbDZVq1ZNY8eOzXd+YmKiTCaT/vzzzwKvCQAAAOCM2HAGAOD8cjKkEeWN+exXDkuefgWe5u7uru7du2vGjBl69dVXZTKZJEmff/65LBaLOnfurHPnzikuLk6DBw9WYGCgFi9erG7duqlq1apq3LhxgZ9htVr14IMPKjw8XGvXrlVqamq+9SHzBAQEaMaMGSpfvry2bNmifv36KSAgQC+99JI6duyorVu3asmSJfZiLSgo6KL3SE9PV+vWrdW0aVOtW7dOx44dU9++fTVgwIB8BeuKFSsUGRmpFStW6M8//1THjh1Vv3599evX77Lfx549e7R69Wp99dVXstlseu6553TgwAFVqlRJknTo0CHdcsstatmypX788UcFBgZq1apV9tmJkyZN0qBBgzRq1Cjdc889Sk1N1apVqwq8fv/28ssva+zYsapSpYpCQkKUnJysNm3a6J133pGXl5dmzZqltm3baufOnYqOjpYkde/eXatXr9b48eMVGxurffv26cSJEzKZTOrdu7emT5+uF154wf4Z06dP1y233KJq1apddT4AAADAGVA+AgBQQnr37q13331XP/30k1q2bCnpQvn00EMPKSgoSEFBQfmKqaefflo//PCDPvvss0KVj8uWLdOOHTv0ww8/qHz5C2XsiBEjLlqn8bXXXrP/c0xMjF544QXNnz9fL730knx8fOTv7y93d3dFRERc9rPmzp2rzMxMzZo1S35+F8rXCRMmqG3btho9erTCw8MlSSEhIZowYYLMZrNq1Kihe++9V8uXL79i+Tht2jTdc889CgkJkSS1bt1a06dP17BhwyRJEydOVFBQkObPny8PDw9J0g033GB//dtvv63nn39eAwcOtB9r1KhRgdfv34YPH64777zT/nVoaKhiY2PtX7/11ltauHChFi1apAEDBmjXrl367LPPtHTpUrVq1UqSVKVKFfv5PXv21NChQ5WQkKDGjRsrJydHc+fOvWg2JAAAAOBKKB8BAM7Pw/fCDESjPruQatSooWbNmmnatGlq2bKl/vzzT/3yyy8aPny4JMlisWjEiBH67LPPdOjQIWVnZysrK6vQazpu375dUVFR9uJRkpo2bXrReQsWLND48eO1Z88enTt3Trm5uQoMDCz095H3WbGxsfbiUZKaN28uq9WqnTt32svH2rVry2z+e7e9yMhIbdmy5bLva7FYNHPmTH3wwQf2Y127dtULL7ygoUOHys3NTYmJibr55pvtxeM/HTt2TIcPH9Ydd9xxVd/PpcTHx+f7+ty5cxo2bJgWL16slJQU5ebm6vz580pKSpJ04RZqs9msW2+99ZLvV758ed17772aNm2aGjdurG+++UZZWVl65JFHrjsrrt3PP/+sd999Vxs2bFBKSooWLlyodu3aXfE1n376qcaMGaPdu3crKChI99xzj959912FhYWVTGgAAAAnwpqPAADnZzJduPXZiMdft08XVp8+ffTll1/q7Nmzmj59uqpWrWovq95991198MEHGjx4sFasWKHExES1bt1a2dnZRXapVq9erS5duqhNmzb69ttvtWnTJr366qtF+hn/9O+C0GQyyWq1Xvb8H374QYcOHVLHjh3l7u4ud3d3derUSQcOHNDy5cslST4+Ppd9/ZWekyQ3twtDH9s/1uq83BqU/yxWJemFF17QwoULNWLECP3yyy9KTExU3bp17deuoM+WpL59+2r+/Pk6f/68pk+fro4dO5bYhkG4tPT0dMXGxmrixImFOn/VqlXq3r27+vTpo23btunzzz9XQkLCFWfzAgAAlGaUjwAAlKAOHTrIzc1Nc+fO1axZs9S7d2/7+o+rVq3SAw88oK5duyo2NlZVqlTRrl27Cv3eNWvWVHJyslJSUuzH1qxZk++c3377TZUqVdKrr76q+Ph4Va9eXQcOHMh3jqenpywWS4GftXnzZqWnp9uPrVq1Sm5ubrrxxhsLnfnfpk6dqk6dOikxMTHfo1OnTvaNZ+rVq6dffvnlkqVhQECAYmJi7EXlv5UtW1aS8l2jf24+cyWrVq1Sz5491b59e9WtW1cRERHav3+//fm6devKarXqp59+uux7tGnTRn5+fpo0aZKWLFmi3r17F+qzUXzuuecevf3222rfvn2hzl+9erViYmL0zDPPqHLlymrRooUef/xxJSQkFHNSAAAA50T5CABACfL391fHjh01ZMgQpaSkqGfPnvbnqlevrqVLl+q3337T9u3b9fjjj+vo0aOFfu9WrVrphhtuUI8ePbR582b98ssvevXVV/OdU716dSUlJWn+/Pnas2ePxo8fr4ULF+Y7JyYmRvv27VNiYqJOnDihrKysiz6rS5cu8vb2Vo8ePbR161atWLFCTz/9tLp162a/5fpqHT9+XN9884169OihOnXq5Ht0795dX3/9tU6dOqUBAwYoLS1NnTp10vr167V7927Nnj1bO3fulCQNGzZM48aN0/jx47V7925t3LhRH374oaQLsxNvuukmjRo1Stu3b9dPP/2Ubw3MK6levbq++uorJSYmavPmzXr00UfzzeKMiYlRjx491Lt3b3399dfat2+fVq5cqc8++8x+jtlsVs+ePTVkyBBVr179krfFw7E1bdpUycnJ+u6772Sz2XT06FF98cUXatOmzRVfl5WVpbS0tHwPAACA0oDyEQCAEtanTx+dPn1arVu3zrc+42uvvaaGDRuqdevWatmypSIiIgpce+6f3NzctHDhQp0/f16NGzdW37599c477+Q75/7779dzzz2nAQMGqH79+vrtt9/0+uuv5zvnoYce0t13363bbrtNZcuW1bx58y76LF9fX/3www86deqUGjVqpIcfflh33HGHJkyYcHUX4x/yNq+51HqNd9xxh3x8fDRnzhyFhYXpxx9/1Llz53TrrbcqLi5OU6ZMsd/i3aNHD73//vv673//q9q1a+u+++7T7t277e81bdo05ebmKi4uTs8++6zefvvtQuV77733FBISombNmqlt27Zq3bq1GjZsmO+cSZMm6eGHH9ZTTz2lGjVqqF+/fvlmh0oX/vyzs7PVq1evq71EcADNmzfXp59+qo4dO8rT01MREREKCgoq8LbtkSNH2jeWCgoKUlRUVAklBgAAMJbJ9s9Fj0qBtLQ0BQUFKTU19aoX1wcAGC8zM1P79u1T5cqV5e3tbXQc4Kr98ssvuuOOO5ScnHzFWaJX+llnPFM8TCZTgRvO/PHHH2rVqpWee+45tW7dWikpKXrxxRfVqFEj+9IAl5KVlZVvFnFaWpqioqL4MwQAAE7pasaj7HYNAABQArKysnT8+HENGzZMjzzyyDXfng5jjRw5Us2bN9eLL74o6cIapH5+frr55pv19ttvKzIy8pKv8/LykpeXV0lGBQAAcAjcdg0AAFAC5s2bp0qVKunMmTMaM2aM0XFwjTIyMuy7pucxm82S8u+iDgAAgAsoHwEAAEpAz549ZbFYtGHDBlWoUMHoOPjLuXPn7LuqS7JvtpSUlCRJGjJkiLp3724/v23btvrqq680adIk7d27V6tWrdIzzzyjxo0b51vDFQAAABdw2zUAAABKrfXr1+u2226zfz1o0CBJFzYumjFjhlJS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zo0xKYDSgPIRQKl07tw5SdLixYuVmJhof/zxxx/2NXaul4+PT6HO++ctKyaTSdKFtX8kadiwYdq2bZvuvfde/fjjj6pVq5YWLlxYJPkAAABgLMakAEoDykcApVKtWrXk5eWlpKQkVatWLd8jKirKft6aNWvs/3z69Gnt2rVLNWvWlCTVrFlTq1atyve+q1at0g033CCz2ay6devKarXmW6/nWtxwww167rnn9H//93968MEHNX369Ot6PwAAADgGxqQASgN3owMAgBECAgL0wgsv6LnnnpPValWLFi2UmpqqVatWKTAwUJUqVZIkDR8+XGFhYQoPD9err76qMmXKqF27dpKk559/Xo0aNdJbb72ljh07avXq1ZowYYL++9//SpJiYmLUo0cP9e7dW+PHj1dsbKwOHDigY8eOqUOHDgVmPH/+vF588UU9/PDDqly5sg4ePKh169bpoYceKrbrAgAAgJLDmBRAaUD5CKDUeuutt1S2bFmNHDlSe/fuVXBwsBo2bKhXXnnFfovJqFGjNHDgQO3evVv169fXN998I09PT0lSw4YN9dlnn2no0KF66623FBkZqeHDh6tnz572z5g0aZJeeeUVPfXUUzp58qSio6P1yiuvFCqf2WzWyZMn1b17dx09elRlypTRgw8+qDfffLPIrwUAAACMwZgUgKtjt2sAuIS8Xf9Onz6t4OBgo+MAAACgFGJMCsAVsOYjAAAAAAAAgGJB+QgAAAAAAACgWHDbNQAAAAAAAIBiwcxHAAAAAAAAAMWC8hEAAAAAAABAsaB8BAAAAAAAAFAsKB8BAAAAAAAAFAvKRwAAAAAAAADFgvIRAAAAAAAAQLGgfAQAAAAAAABQLCgfAQAAAAAAABSL/weIYyXO5QM9CwAAAABJRU5ErkJggg==",
            "text/plain": [
              "<Figure size 1600x800 with 2 Axes>"
            ]
          },
          "metadata": {},
          "output_type": "display_data"
        }
      ],
      "source": [
        "# Learning curves \n",
        "\n",
        "acc = history.history['accuracy']\n",
        "val_acc = history.history['val_accuracy']\n",
        "loss=history.history['loss']\n",
        "val_loss=history.history['val_loss']\n",
        "\n",
        "plt.figure(figsize=(16,8))\n",
        "plt.subplot(1, 2, 1)\n",
        "plt.plot(acc, label='Training Accuracy')\n",
        "plt.plot(val_acc, label='Validation Accuracy')\n",
        "plt.legend(loc='lower right')\n",
        "plt.title('Training and Validation Accuracy')\n",
        "plt.xlabel(\"epochs\")\n",
        "plt.ylabel(\"accuracy\")\n",
        "\n",
        "plt.subplot(1, 2, 2)\n",
        "plt.plot(loss, label='Training Loss')\n",
        "plt.plot(val_loss, label='Validation Loss')\n",
        "plt.legend(loc='upper right')\n",
        "plt.title('Training and Validation Loss')\n",
        "plt.xlabel(\"epochs\")\n",
        "plt.ylabel(\"loss\")\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "I_PRZPplHqmV"
      },
      "source": [
        "## LSTM"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 67,
      "metadata": {
        "id": "-T3A0-TWmDS8"
      },
      "outputs": [],
      "source": [
        "def define_model3(vocab_size, max_length):\n",
        "    model3 = Sequential()\n",
        "    model3.add(Embedding(vocab_size,300, input_length=max_length))\n",
        "    model3.add(LSTM(500))\n",
        "    model3.add(Dense(10, activation='softmax'))\n",
        "    \n",
        "    model3.compile(loss = 'categorical_crossentropy',optimizer = 'adam',metrics = ['accuracy'])\n",
        "    \n",
        "    # summarize defined model\n",
        "    model3.summary()\n",
        "    return model3"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 68,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "iNtO1edjHxt6",
        "outputId": "649205f4-53fa-4ba1-909b-827dab404f80"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Model: \"sequential_2\"\n",
            "_________________________________________________________________\n",
            " Layer (type)                Output Shape              Param #   \n",
            "=================================================================\n",
            " embedding_2 (Embedding)     (None, 10, 300)           19800     \n",
            "                                                                 \n",
            " lstm (LSTM)                 (None, 500)               1602000   \n",
            "                                                                 \n",
            " dense_3 (Dense)             (None, 10)                5010      \n",
            "                                                                 \n",
            "=================================================================\n",
            "Total params: 1626810 (6.21 MB)\n",
            "Trainable params: 1626810 (6.21 MB)\n",
            "Non-trainable params: 0 (0.00 Byte)\n",
            "_________________________________________________________________\n"
          ]
        }
      ],
      "source": [
        "model3 = define_model3(vocab_size, max_length)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 69,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "FGq3NSaJCoJg",
        "outputId": "8bbbeb09-6b9c-45c8-ef4e-38beb1ffa860"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Epoch 1/15\n",
            "1/1 [==============================] - 1s 1s/step - loss: 2.2959 - accuracy: 0.3333 - val_loss: 2.2928 - val_accuracy: 0.2000\n",
            "Epoch 2/15\n",
            "1/1 [==============================] - 0s 46ms/step - loss: 2.2423 - accuracy: 0.5000 - val_loss: 2.2842 - val_accuracy: 0.1000\n",
            "Epoch 3/15\n",
            "1/1 [==============================] - 0s 44ms/step - loss: 2.1854 - accuracy: 0.5000 - val_loss: 2.2782 - val_accuracy: 0.1000\n",
            "Epoch 4/15\n",
            "1/1 [==============================] - 0s 44ms/step - loss: 2.1187 - accuracy: 0.5000 - val_loss: 2.2797 - val_accuracy: 0.1000\n",
            "Epoch 5/15\n",
            "1/1 [==============================] - 0s 44ms/step - loss: 2.0375 - accuracy: 0.5000 - val_loss: 2.3030 - val_accuracy: 0.1000\n",
            "Epoch 6/15\n",
            "1/1 [==============================] - 0s 44ms/step - loss: 1.9434 - accuracy: 0.4167 - val_loss: 2.3677 - val_accuracy: 0.1000\n",
            "Epoch 7/15\n",
            "1/1 [==============================] - 0s 44ms/step - loss: 1.8487 - accuracy: 0.4167 - val_loss: 2.4466 - val_accuracy: 0.0000e+00\n",
            "Epoch 8/15\n",
            "1/1 [==============================] - 0s 45ms/step - loss: 1.7499 - accuracy: 0.4167 - val_loss: 2.4474 - val_accuracy: 0.1000\n",
            "Epoch 9/15\n",
            "1/1 [==============================] - 0s 48ms/step - loss: 1.6067 - accuracy: 0.5000 - val_loss: 2.3739 - val_accuracy: 0.1000\n",
            "Epoch 10/15\n",
            "1/1 [==============================] - 0s 46ms/step - loss: 1.4372 - accuracy: 0.6667 - val_loss: 2.2982 - val_accuracy: 0.2000\n",
            "Epoch 11/15\n",
            "1/1 [==============================] - 0s 47ms/step - loss: 1.3102 - accuracy: 0.6667 - val_loss: 2.3062 - val_accuracy: 0.1000\n",
            "Epoch 12/15\n",
            "1/1 [==============================] - 0s 46ms/step - loss: 1.2487 - accuracy: 0.6667 - val_loss: 2.3917 - val_accuracy: 0.2000\n",
            "Epoch 13/15\n",
            "1/1 [==============================] - 0s 48ms/step - loss: 1.1563 - accuracy: 0.6667 - val_loss: 2.5326 - val_accuracy: 0.3000\n",
            "Epoch 14/15\n",
            "1/1 [==============================] - 0s 51ms/step - loss: 0.9971 - accuracy: 0.6667 - val_loss: 2.7259 - val_accuracy: 0.1000\n",
            "Epoch 15/15\n",
            "1/1 [==============================] - 0s 48ms/step - loss: 0.8249 - accuracy: 0.7500 - val_loss: 2.9104 - val_accuracy: 0.1000\n"
          ]
        }
      ],
      "source": [
        "history = model3.fit(X_train, y_train, epochs=15, verbose=1,validation_data=(X_test,y_test))"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 70,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 513
        },
        "id": "36X8FbbgOhTf",
        "outputId": "d559e43f-df22-46de-a7a1-ec3c9cab5e07"
      },
      "outputs": [
        {
          "data": {
            "image/png": "iVBORw0KGgoAAAANSUhEUgAABR8AAAK9CAYAAACtshu3AAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8WgzjOAAAACXBIWXMAAA9hAAAPYQGoP6dpAAEAAElEQVR4nOzdd3QU5dvG8e/uppFOSEgooYUACV2agHSQrigiItIUbGDDioWmL6jY8afYABuiIE1BamhSpHcIhF4DAUJIQtruvH8sRCIdEibl+pwzh9nZmdlrNxEf7n2KxTAMAxEREREREREREZFsZjU7gIiIiIiIiIiIiORPKj6KiIiIiIiIiIhIjlDxUURERERERERERHKEio8iIiIiIiIiIiKSI1R8FBERERERERERkRyh4qOIiIiIiIiIiIjkCBUfRUREREREREREJEeo+CgiIiIiIiIiIiI5QsVHERERERERERERyREqPorkAb1796ZMmTI3de3QoUOxWCzZGyiX2bdvHxaLhfHjx9/217ZYLAwdOjTz8fjx47FYLOzbt++a15YpU4bevXtna55b+V0RERERuV3Uvr06tW//pfatSN6n4qPILbBYLNe1LVq0yOyoBd6zzz6LxWIhJibmiue88cYbWCwWNm3adBuT3bgjR44wdOhQNmzYYHaUy9q+fTsWiwUPDw/i4+PNjiMiIiI3QO3bvEPt25x1oQD8wQcfmB1FJM9zMTuASF72448/Znn8ww8/MG/evEuOR0RE3NLrfPPNNzgcjpu69s033+S11167pdfPD7p3787o0aOZMGECgwcPvuw5v/zyC1WrVqVatWo3/To9evTgoYcewt3d/abvcS1Hjhxh2LBhlClThho1amR57lZ+V7LLTz/9REhICKdPn2by5Mn07dvX1DwiIiJy/dS+zTvUvhWRvELFR5Fb8Mgjj2R5vHLlSubNm3fJ8f9KTk7G09Pzul/H1dX1pvIBuLi44OKi/9Tr1atH+fLl+eWXXy7bOFuxYgV79+7l3XffvaXXsdls2Gy2W7rHrbiV35XsYBgGEyZM4OGHH2bv3r38/PPPubb4mJSUhJeXl9kxREREchW1b/MOtW9FJK/QsGuRHNa0aVOqVKnC2rVrady4MZ6enrz++usATJ8+nfbt21O8eHHc3d0JCwvj7bffxm63Z7nHf+c5uXgIwNdff01Y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UoSKFSuyfft2AJ599lmeeuop5s6dS8uWLencuXPm+3rqqafo3Lkz69at4+6776ZTp06ZRczcRnM+ioiIiIiIiIjkcRaLBU83F1M2i8WSbe/Dy8sry+OXXnqJqVOnMmLECJYuXcqGDRuoWrUqaWlpV72Pq6vrJZ/P1QqFlzv/eueyzCl9+/Zlz5499OjRg82bN1O7dm1Gjx4NQNu2bdm/fz8vvPACR44coUWLFrz00kum5r0SFR9FRERERERERCRXWrZsGb179+a+++6jatWqhISEsG/fvtuawc/Pj+DgYFavXp15zG63s27dupu+Z0REBBkZGfzzzz+Zx06ePEl0dDSRkZGZx0JDQ3nyySeZMmUKL774It98803mc0FBQfTq1YuffvqJTz75hK+//vqm8+QkDbsWEREREREREZFcKTw8nClTptCxY0csFgtvvfXWTQ91vhXPPPMMI0eOpHz58lSqVInRo0dz+vTp6+r1uXnzZnx8fDIfWywWqlevzr333ku/fv346quv8PHx4bXXXqNEiRLce++9ADz//PO0bduWChUqcPr0aRYuXEhERAQAgwcPplatWlSuXJnU1FT+/PPPzOdyGxUfRUREREREREQkV/roo4949NFHadCgAYGBgbz66qskJCTc9hyvvvoqx44do2fPnthsNh5//HFat26NzXbt+S4bN26c5bHNZiMjI4Nx48bx3HPP0aFDB9LS0mjcuDGzZs3KHAJut9vp378/hw4dwtfXlzZt2vDxxx8D4ObmxqBBg9i3bx+FChWiUaNGTJw4MfvfeDawGGYPYL/NEhIS8PPz48yZM/j6+podR0REROSGqT2T9+lnKCIityolJYW9e/dStmxZPDw8zI5T4DgcDiIiInjwwQd5++23zY6TI672O3YjbRn1fBQREREREREREbmK/fv3M3fuXJo0aUJqaiqff/45e/fu5eGHHzY7Wq6nBWdEREREssnmQ2f4fe0hHI4CNbBEREREJN+zWq2MHz+eOnXq0LBhQzZv3sz8+fNz3zyLhgFnj4I9w+wkmdTzUURERCQbOBwGb03fwoaD8Rw6fY7nWoabHUlEREREskloaCjLli0zO8a1JcbC2WNw7jQERcB1LIiT09TzUURERCQb/L7uEBsOxuPt7kK3uqFmxxERERGRgiY10dnrEcA7OFcUHkHFRxEREZFblpCS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juS1O5twT4uqWoxGREq1AhUf77rrrjxfWywWKlasyA033MCECRMKI1eJlbvKtYZci4iIiFyTZcuW5Sk8ApQvX54333xTH4iLiBE3Nw6habUgnp0Xw6p9J3nuq00s332M/97VhABvD9PxRESMKFDx0WazFXaOUsFms/PnznPFRw25FhEREbkmXl5epKSkXLD99OnTeHp6GkgkIgKVg3z4fFBbPvhzD+/+tptvY46w4eDfTO4dTniNsqbjiYgUO82AW4w2H07i+OkMArzcaRVa7spvEBEREZFLuv322xk8eDCrV6/Gbrdjt9tZtWoVQ4YM4Y477jAdT0RKMTerhWE31GP+4+2oVtaHuJNnuH9aNO//uQebzW46nohIsSpQ8fHee+/lrbfeumD7uHHjuP/++685VEmVM+S6U/0KeLip7isiIiJyLSZPnkydOnVo164d3t7eeHt70759e+rWrcvEiRNNxxMRIaJmWX56phO3N6tMls3OuMU76TdjNYnJZ01HExEpNgWqgC1fvpxbb731gu09evRg+fLl1xyqpPp9RyIA12u+RxEREZFrVqZMGb799lt27drF119/zddff82uXbtYuHAhZcqUMR1PRASAQG8P3usTzrj7muHj4cbKvSe4ZeJyfvsr0XQ0EZFiUaA5Hy81j46HhwfJycnXHKokOpp8lq2Hk7FYoKuKjyIiIiIFMmLEiMu+/scff+S233nnnaKOIyKSLxaLhQdaVieiZlmenruRbUeSGfTpOga0D+VfPRrg7eFmOqKISJEpUPGxadOmzJs3jzFjxuTZ/uWXX9KoUaNCCVbS/HFuoZlm1cpQMcDLcBoRERER17Rx48Z87WexWIo4iYjI1atT0Z8FT7Zn3OKdzFixn9krD7Bq3wne6xNOveAA0/FERIpEgYqPL730Evfccw979+7lhhtuAGDp0qXMnTuXr776qlADlhQ58z3eoF6PIiIiIgX2z56NIiKuyMvdjZdub0THehUYOX8TOxJS6DllBS/3bEzvVtX14YmIlDgFmvOxZ8+eLFq0iD179vDkk0/y3HPPcejQIX777TfuuuuuQo7o+tKzsoncfRyAGxuq+CgiIiIiIlLaXX9dJX4e3olO9SpwNtPG6AVbePLzDSSlZZqOJiJSqArU8xHgtttu47bbbivMLCXWmv0nScvIplKAF42rBJqOIyIiIiIi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kRJAxUcRERERERERwWq18MY9TekZVoUsm50hn21g5Z7jpmOJiItT8VFEREREREREAHCzWnjngTC6NaxERpaNQZ+uY33s36ZjiYgLU/FRRERERERERHJ5uFmZ0rcFHetWIC0jmwGz1rD1cJLpWCLiolR8FBEREREREZE8vD3c+Kh/BC1rliXlbBb9Z65hz9EU07FExAU5RfFx6tSphIaG4u3tTZs2bVizZs0l912wYAEtW7akTJky+Pn50bx5c+bMmVOMaUVERERERERKPl9Pd2YObEXTqkGcTM2g7/TVxJ5INR1LRFyM8eLjvHnzGDFiBC+//DIbNmwgLCyM7t27c/To0YvuX65cOV588UWio6PZvHkzAwcOZODAgfzyyy/FnFxERERERESkZAv09uCTR1pTP9ifoynp9J2+mvikM6ZjiYgLsdjtdrvJAG3atKFVq1ZMmTIFAJvNRvXq1Xnqqaf417/+la9jtGjRgttuu43XXnvtivsmJycTFBREUlISgYGB15RdRESkVEmOh4xUqFDXdJJST/czrk8/QxFxNUeTz/LAh9EcOJFG7Qp+zHu8HRUDvEzHEhFDruZexmjPx4yMDNavX0+3bt1yt1mtVrp160Z0dPQV32+321m6dCk7d+6kc+fOF90nPT2d5OTkPA8RERG5ShmpMP16mNYRUhJMpxEREZFiVinQm88GtaFKkDf7jqfy0IzVnErLMB1LRFyA0eLj8ePHyc7OJjg4OM/24OBgEhIu/R+bpKQk/P398fT05LbbbuO9997jpptuuui+Y8eOJSgoKPdRvXr1Qv0eRERESoV1MyElHrLOwP7lptOIiIiIAdXK+vL5Y22p4O/FjoQUHp61ltPpWaZjiYiTMz7nY0EEBAQQExPD2rVref311xkxYgR//vnnRfcdPXo0SUlJuY+4uLjiDSsiIuLqMs9A1OTzXx9YYS6LiIiIGFWrgh+fD2pDGV8PNsWd4pHZazmTkW06log4MaPFxwoVKuDm5kZiYmKe7YmJiYSEhFzyfVarlbp169K8eXOee+457rvvPsaOHXvRfb28vAgMDMzzEBERkauw/hNIPQpWd8fXsVFm84iIiIhR14UEMOeRNgR4ubNm/0mGfLae9CwVIEXk4owWHz09PYmIiGDp0qW522w2G0uXLqVdu3b5Po7NZiM9Pb0oIoqIiJRumWchaqKj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lo+AX4VrP6YYkZ2dnVt4LF++vOk4IkXCx8cx3Obo0aNUqlRJQ7BFRERESrDq5XyZ3Duch2et4cu1cYRVL0Of1jVMxyo0WnBGRJxP+6fBzQviVsGByMI55r4/4dBacPd2HF9cVs4cj76+voaTiBStnN9xzWsqIiIiUvJ1rl+RkTdfB8DL325j48G/DScqPCo+iojzCawMLfo72svGFc4xl59b4TpiAAQEF84xxSgNtZaSTr/jIiIiIqXLk13r0L1xMBnZNp74bAPHUtJNRyoUKj6KiHPqOBysHo6ej7HR13asAysgNgrcPKHDM4UST0RERERERKQwWSwWxt8fRp2KfiQkn2XoFxvIzLaZjnXNVHwUEecUVA3CH3S0l19j78ec3pPhD0FglWs7loiTCQ0NZeLEifne/88//8RisWilcBERERERJxTg7cFH/Vvi7+XOmv0neeOn7aYjXTMVH0XEeXUcAVZ3x6rXh9YV7BgHV8P+ZY5elB2fLdx8IlfBYrFc9vHKK68U6Lhr165l8ODB+d6/ffv2xMfHExQUVKDzFUSDBg3w8vIiISGh2M4pIiIiIuKq6lT0Z8IDYQDMijrAwo2HDCe6Nio+iojzKlsTmvV2tAs692NOr8nmfaBM9cLJJVIA8fHxuY+JEycSGBiYZ9vIkSNz97Xb7WRlZeXruBUrVryqxXc8PT0JCQkptvkEV6xYwZkzZ7jvvvv45JNPiuWcl6PFW0RERETEFXRvHMKw6+sCMHrBFrYdSTKcqOBUfBQR59ZpBFissPsXOLLx6t57aD3s+Q0sbo5elFJi2e120jKyjDzsdnu+MoaEhOQ+goKCsFgsuV/v2LGDgIAAfv75ZyIiIvDy8mLFihXs3buXO++8k+DgYPz9/WnVqhW//fZbnuP+77Bri8XCxx9/zN13342vry/16tXju+++y339f4ddz549mzJlyvDLL7/QsGFD/P39ueWWW4iPj899T1ZWFk8//TRlypShfPnyjBo1iocffpi77rrrit/3jBkz6Nu3Lw899BAzZ8684PVDhw7Rp08fypUrh5+fHy1btmT16tW5r3///fe0atUKb29vKlSowN13353ne120aFGe45UpU4bZs2cDcODAASwWC/PmzaNLly54e3vz+eefc+LECfr06UPVqlXx9fWladOmzJ07N89xbDYb48aNo27dunh5eVGj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5+Hr6IFo6tz51KBBA9q3b8/MmTPp2rUre/bsITIykldffRWA7Oxs3njjDebPn8/hw4fJyMggPT0933M6bt++nerVq+cWHoGLLsg2b948Jk+ezN69ezl9+jRZWVkEBgbm+/vIOVdYWFhu4RGgQ4cO2Gw2du7cmVt8bNy4MW5u51fbq1y5Mlu2bLnkcbOzs/nkk0+YNGlS7rZ+/foxcuRIxowZg9VqJSYmhk6dOuUWHv/p6NGjHDlyhBtvvPGqvp+LadmyZZ6vT58+zSuvvMKPP/5IfHw8WVlZnDlzhoMHDwKOIdRubm506dLloserUqUKt912GzNnzqR169Z8//33pKenazSHiIiIiJRoxud8FBERuWYWi2Pos4nHueHT+fXoo4/yzTffkJKSwqxZs6hTp05usertt99m0qRJjBo1ij/++IOYmBi6d+9ORkZGoV2q6OhoHnzwQW699VZ++OEHNm7cyIsvvlio5/in/y0QWiwWbDbbJff/5ZdfOHz4ML169cLd3R13d3d69+5NbGwsS5cuBcDHx+eS77/cawBWq+PWx/6PuTovNQflPwurACNHjmThwoW88cYbREZGEhMTQ9OmTXOv3ZXODTBo0CC+/PJLzpw5w6xZs+jVq1exLRgkIiIiImKCio8iIiLF6IEHHsBqtfLFF1/w6aef8sgjj+TO/xgVFcWdd95Jv379CAsLo3bt2uzatSvfx27YsCFxcXF5FmpbtWpVnn1WrlxJzZo1efHFF2nZsiX16tUjNjY2zz6enp5kZ2df8VybNm0iNTU1d1tUVBRWq5Xrrrsu35n/14wZM+jduzcxMTF5Hr17985deKZZs2ZERkZetGgYEBBAaGhobqHyf1WsWBEgzzX65+IzlxMVFcWAAQO4++67adq0KSEhIRw4cCD39aZNm2Kz2Vi2bNklj3Hrrbfi5+fHBx98wOLFi3nkkUfydW4REREREVel4qOIiEgx8vf3p1evXowePZr4+HgGDBiQ+1q9evVYsmQJK1euZPv27Tz++OMkJibm+9jdunWjfv36PPzww2zatInIyEhefPHFPPvUq1ePgwcP8uWXX7J3714mT57MwoUL8+wTGhrK/v37iYmJ4fjx46Snp19wrgcffBBvb28efvhhtm7dyh9//MFTTz3FQw89lDvk+modO3aM77//nocffpgmTZrkefTv359FixZx8uRJhg0bRnJyMr1792bdunXs3r2bOXPmsHPnTgBeeeUVJkyYwOTJk9m9ezcbNmzgvffeAxy9E9u2bcubb77J9u3bWbZsWZ45MC+nXr16LFiwgJiYGDZt2kTfvn3z9OIMDQ3l4Ycf5pFHHmHRokXs37+fP//8k/nz5+fu4+bmxoABAxg9ejT16tW76LB4EREREZGSRMVHERGRYvboo4/y999/07179zzzM/773/+mRYsWdO/ena5duxISEsJdd92V7+NarVYWLlzImTNnaN26NYMGDeL111/Ps88dd9zBs88+y7Bhw2jevDkrV67kpZdeyrPPvffeyy233ML1119PxYoVmTt37gXn8vX15ZdffuHkyZO0atWK++67jxtvvJEpU6Zc3cX4h5zFay42X+ONN96Ij48Pn332GeXLl+f333/n9OnTdOnShYiICKZPn547xPvhhx9m4sSJvP/++zRu3Jjbb7+d3bt35x5r5syZZGVlERERwfDhw/nvf/+br3zvvPMOZcuWpX379vTs2ZPu3bvTokWLPPt88MEH3HfffTz55JM0aNCAxx57LE/vUHD8/DMyMhg4cODVXiIREREREZdjsf9z0qNSIDk5maCgIJKSkq56cn0RETHv7Nmz7N+/n1q1auHt7W06jshVi4yM5MYbbyQuLu6yvUQv97uu+xnXp5+hiIiIuLKruZfRatciIiIixSA9PZ1jx47xyiuvcP/99xd4eLqIiIiIiCvRsGsRERGRYjB37lxq1qzJqVOnGDdunOk4IiIiIiLFQsVHERERkWIwYMAAsrOzWb9+PVWrVjUdR0RERESkWKj4KCIiIiIiIiIiIkVCxUcREXFJpWy9NCmF9DsuIiIiIiWBio8iIuJSPDw8AEhLSzOcRKRo5fyO5/zOi4iIiIi4Iq12LSIiLsXNzY0yZcpw9OhRAHx9fbFYLIZTiRQeu91OWloaR48epUyZMri5uZmOJCIiIiJSYCo+ioiIywkJCQHILUCKlERlypTJ/V0XEREREXFVKj6KiIjLsVgsVK5cmUqVKpGZmWk6jkih8/DwUI9HERERESkRVHwUERGX5ebmpgKNiIiIiIiIE9OCMyIiIiIiIiIiIlIkVHwUERERERERERGRIqHio4iIiIiIiIiIiBSJUjfno91uByA5OdlwEhEREZGCybmPybmvEdeje1IRERFxZVdz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",
            "text/plain": [
              "<Figure size 1600x800 with 2 Axes>"
            ]
          },
          "metadata": {},
          "output_type": "display_data"
        }
      ],
      "source": [
        "# Learning curves \n",
        "\n",
        "acc = history.history['accuracy']\n",
        "val_acc = history.history['val_accuracy']\n",
        "loss=history.history['loss']\n",
        "val_loss=history.history['val_loss']\n",
        "\n",
        "plt.figure(figsize=(16,8))\n",
        "plt.subplot(1, 2, 1)\n",
        "plt.plot(acc, label='Training Accuracy')\n",
        "plt.plot(val_acc, label='Validation Accuracy')\n",
        "plt.legend(loc='lower right')\n",
        "plt.title('Training and Validation Accuracy')\n",
        "plt.xlabel(\"epochs\")\n",
        "plt.ylabel(\"accuracy\")\n",
        "\n",
        "plt.subplot(1, 2, 2)\n",
        "plt.plot(loss, label='Training Loss')\n",
        "plt.plot(val_loss, label='Validation Loss')\n",
        "plt.legend(loc='upper right')\n",
        "plt.title('Training and Validation Loss')\n",
        "plt.xlabel(\"epochs\")\n",
        "plt.ylabel(\"loss\")\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "qBmXCUoUct-Y"
      },
      "source": [
        "## GRU"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 71,
      "metadata": {
        "id": "xzIyloY3cyoD"
      },
      "outputs": [],
      "source": [
        "def define_model3(vocab_size, max_length):\n",
        "    model3 = Sequential()\n",
        "    model3.add(Embedding(vocab_size,300, input_length=max_length))\n",
        "    model3.add(GRU(500))\n",
        "    model3.add(Dense(10, activation='softmax'))\n",
        "    \n",
        "    model3.compile(loss = 'categorical_crossentropy',optimizer = 'adam',metrics = ['accuracy'])\n",
        "    \n",
        "    # summarize defined model\n",
        "    model3.summary()\n",
        "    return model3"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 72,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "qEXaR-g4cylS",
        "outputId": "b8071e06-098e-4878-fae7-84a628aa0673"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Model: \"sequential_3\"\n",
            "_________________________________________________________________\n",
            " Layer (type)                Output Shape              Param #   \n",
            "=================================================================\n",
            " embedding_3 (Embedding)     (None, 10, 300)           19800     \n",
            "                                                                 \n",
            " gru (GRU)                   (None, 500)               1203000   \n",
            "                                                                 \n",
            " dense_4 (Dense)             (None, 10)                5010      \n",
            "                                                                 \n",
            "=================================================================\n",
            "Total params: 1227810 (4.68 MB)\n",
            "Trainable params: 1227810 (4.68 MB)\n",
            "Non-trainable params: 0 (0.00 Byte)\n",
            "_________________________________________________________________\n"
          ]
        }
      ],
      "source": [
        "model3 = define_model3(vocab_size, max_length)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 73,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "49hqm9sWc1ED",
        "outputId": "b5da6e36-1690-4bd7-9f26-4706bf58a724"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Epoch 1/15\n",
            "1/1 [==============================] - 1s 1s/step - loss: 2.2984 - accuracy: 0.2500 - val_loss: 2.2994 - val_accuracy: 0.1000\n",
            "Epoch 2/15\n",
            "1/1 [==============================] - 0s 42ms/step - loss: 2.2320 - accuracy: 0.4167 - val_loss: 2.3012 - val_accuracy: 0.1000\n",
            "Epoch 3/15\n",
            "1/1 [==============================] - 0s 42ms/step - loss: 2.1667 - accuracy: 0.4167 - val_loss: 2.3114 - val_accuracy: 0.1000\n",
            "Epoch 4/15\n",
            "1/1 [==============================] - 0s 41ms/step - loss: 2.0985 - accuracy: 0.4167 - val_loss: 2.3362 - val_accuracy: 0.1000\n",
            "Epoch 5/15\n",
            "1/1 [==============================] - 0s 39ms/step - loss: 2.0273 - accuracy: 0.4167 - val_loss: 2.3836 - val_accuracy: 0.1000\n",
            "Epoch 6/15\n",
            "1/1 [==============================] - 0s 41ms/step - loss: 1.9567 - accuracy: 0.4167 - val_loss: 2.4494 - val_accuracy: 0.2000\n",
            "Epoch 7/15\n",
            "1/1 [==============================] - 0s 42ms/step - loss: 1.8872 - accuracy: 0.4167 - val_loss: 2.4948 - val_accuracy: 0.2000\n",
            "Epoch 8/15\n",
            "1/1 [==============================] - 0s 39ms/step - loss: 1.8017 - accuracy: 0.4167 - val_loss: 2.4850 - val_accuracy: 0.1000\n",
            "Epoch 9/15\n",
            "1/1 [==============================] - 0s 40ms/step - loss: 1.6796 - accuracy: 0.4167 - val_loss: 2.4210 - val_accuracy: 0.0000e+00\n",
            "Epoch 10/15\n",
            "1/1 [==============================] - 0s 40ms/step - loss: 1.5225 - accuracy: 0.5833 - val_loss: 2.3237 - val_accuracy: 0.0000e+00\n",
            "Epoch 11/15\n",
            "1/1 [==============================] - 0s 40ms/step - loss: 1.3597 - accuracy: 0.5833 - val_loss: 2.2507 - val_accuracy: 0.1000\n",
            "Epoch 12/15\n",
            "1/1 [==============================] - 0s 40ms/step - loss: 1.2671 - accuracy: 0.6667 - val_loss: 2.2699 - val_accuracy: 0.1000\n",
            "Epoch 13/15\n",
            "1/1 [==============================] - 0s 43ms/step - loss: 1.2455 - accuracy: 0.5833 - val_loss: 2.3308 - val_accuracy: 0.0000e+00\n",
            "Epoch 14/15\n",
            "1/1 [==============================] - 0s 41ms/step - loss: 1.1315 - accuracy: 0.5833 - val_loss: 2.4571 - val_accuracy: 0.0000e+00\n",
            "Epoch 15/15\n",
            "1/1 [==============================] - 0s 44ms/step - loss: 0.9986 - accuracy: 0.5833 - val_loss: 2.6613 - val_accuracy: 0.2000\n"
          ]
        }
      ],
      "source": [
        "history = model3.fit(X_train, y_train, epochs=15, verbose=1,validation_data=(X_test,y_test))"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 74,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 513
        },
        "id": "xDKC13iBc3Bw",
        "outputId": "fb4ff52f-419b-4d2f-d781-446632aa796d"
      },
      "outputs": [
        {
          "data": {
            "image/png": "iVBORw0KGgoAAAANSUhEUgAABR8AAAK9CAYAAACtshu3AAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8WgzjOAAAACXBIWXMAAA9hAAAPYQGoP6dpAAEAAElEQVR4nOzdd3QUZd/G8e9m00gFUmihJvTeBaRpqIqAiKJIE7AAKiJ2RUBfeRQLCgpWEBFBkGKlSg0dpBcJhE7oSUhC2u68fyysxlACJJmU63POHnZnp1yzG2Dym7tYDMMwEBEREREREREREcliLmYHEBERERERERERkfxJxUcRERERERERERHJFio+ioiIiIiIiIiISLZQ8VFERERERERERESyhYqPIiIiIiIiIiIiki1UfBQREREREREREZFsoeKjiIiIiIiIiIiIZAsVH0VERERERERERCRbqPgoIiIiIiIiIiIi2ULFR5E8oG/fvpQrV+6Wth05ciQWiyVrA+Uyhw4dwmKxMGXKlBw/tsViYeTIkc7XU6ZMwWKxcOjQoRtuW65cOfr27ZuleW7nZ0VEREQkp+j69vp0ffsPXd+K5H0qPorcBovFkqnH8uXLzY5a4D3zzDNYLBYiIyOvuc5rr72GxWJh+/btOZjs5p04cYKRI0eydetWs6Nc1Z49e7BYLHh6ehITE2N2HBEREbkJur7NO3R9m72uFIDff/99s6OI5HmuZgcQycu+++67dK+nTp3K4sWLMyyvWrXqbR3nyy+/xG6339K2r7/+Oi+//PJtHT8/6NmzJ+PHj2f69OmMGDHiquv88MMP1KxZk1q1at3ycXr16kWPHj3w8PC45X3cyIkTJxg1ahTlypWjTp066d67nZ+VrDJt2jSKFy/OhQsXmD17NgMGDDA1j4iIiGSerm/zDl3fikheoeKjyG149NFH071et24dixcvzrD8vxITE/Hy8sr0cdzc3G4pH4Crqyuurvqr3rhxY8LCwvjhhx+uenG2du1aoqKi+N///ndbx7FarVit1tvax+24nZ+VrGAYBtOnT+eRRx4hKiqK77//PtcWHxMSEvD29jY7hoiISK6i69u8Q9e3IpJXqNu1SDZr1aoVNWrUYPPmzbRo0QIvLy9effVVAObPn88999xDyZIl8fDwIDQ0lLfeegubzZZuH/8d5+TfXQC++OILQkND8fDwoGHDhmzcuDHdtlcbE8disTBkyBDmzZtHjRo18PDwoHr16ixYsCBD/uXLl9OgQQM8PT0JDQ3l888/z/Q4O6tWraJ79+6UKVMGDw8PSpcuzXPPPcelS5cynJ+Pjw/Hjx+nS5cu+Pj4EBQUxPDhwzN8FjExMfTt2xd/f38KFy5Mnz59Mt21t2fPnuzdu5ctW7ZkeG/69OlYLBYefvhhUlJSGDFiBPXr18ff3x9vb2+aN2/OsmXLbniMq42JYxgGb7/9NiEhIXh5edG6dWt27dqVYdvz588zfPhwatasiY+PD35+fnTo0IFt27Y511m+fDkNGzYEoF+/fs6uT1fGA7ramDgJCQk8//zzlC5dGg8PDypXrsz777+PYRjp1ruZn4triYiI4NChQ/To0YMePXqwcuVKjh07lmE9u93Oxx9/TM2aNfH09CQoKIj27duzadOmdOtNmzaNRo0a4eXlRZEiRWjRogWLFi1Kl/nfYxJd8d/xhq58LytWrGDQoEEEBwcTEhICwOHDhxk0aBCVK1emUKFCBAQE0L1796uOaxQTE8Nzzz1HuXLl8PDwICQkhN69e3P27Fni4+Px9vbm2WefzbDdsWPHsFqtjBkzJpOfpIiISO6l61td3xak69sbOX36NP3796dYsWJ4enpSu3Ztvv322wzrzZgxg/r16+Pr64ufnx81a9bk448/dr6fmprKqFGjqFixIp6engQEBHDnnXeyePHiLMsqYhbdLhLJAefOnaNDhw706NGDRx99lGLFigGO/8h9fHwYNmwYPj4+/Pnnn4wYMYK4uDjGjh17w/1Onz6dixcv8sQTT2CxWHjvvfe4//77OXjw4A3vEK5evZo5c+YwaNAgfH19+eSTT+jWrRtHjhwhICAAgL/++ov27dtTokQJRo0ahc1mY/To0QQFBWXqvGfNmkViYiJPPfUUAQEBbNiwgfHjx3Ps2DFmzZqVbl2bzUa7du1o3Lgx77//PkuWLOGDDz4gNDSUp556CnBc5HTu3JnVq1fz5JNPUrVqVebOnUufPn0yladnz56MGjWK6dOnU69evXTH/vHHH2nevDllypTh7NmzfPXVVzz88MMMHDiQixcv8vXXX9OuXTs2bNiQoSvIjYwYMYK3336bjh070rFjR7Zs2ULbtm1JSUlJt97BgweZN28e3bt3p3z58pw6dYrPP/+cli1bsnv3bkqWLEnVqlUZPXo0I0aM4PHHH6d58+YANG3a9KrHNgyD++67j2XLltG/f3/q1KnDwoULeeGFFzh+/DgfffRRuvUz83NxPd9//z2hoaE0bNiQGjVq4OXlxQ8//MALL7yQbr3+/fszZcoUOnTowIABA0hLS2PVqlWsW7eOBg0aADBq1ChGjhxJ06ZNGT16NO7u7qxfv54///yTtm3bZvrz/7dBgwYRFBTEiBEjSEhIAGDjxo2sWbOGHj16EBISwqFDh5g4cSKtWrVi9+7dzlYc8fHxNG/enD179vDYY49Rr149zp49y88//8yxY8eoU6cOXbt2ZebMmXz44YfpWgj88MMPGIZBz549bym3iIhIbqPrW13fFpTr2+u5dOkSrVq1IjIykiFDhlC+fHlmzZpF3759iYmJcd6UXrx4MQ8//DB333037777LuAYJz0iIsK5zsiRIxkzZgwDBgygUaNGxMXFsWnTJrZs2UKbNm1uK6eI6QwRyTKDBw82/vvXqmXLlgZgTJo0KcP6iYmJGZY98cQThpeXl5GUlORc1qdPH6Ns2bLO11FRUQZgBAQEGOfPn3cunz9/vgEYv/zyi3PZm2++mSETYLi7uxuRkZHOZdu2bTMAY/z48c5lnTp1Mry8vIzjx487l+3fv99wdXXNsM+rudr5jRkzxrBYLMbhw4fTnR9gjB49Ot26devWNerXr+98PW/ePAMw3nvvPeeytLQ0o3nz5gZgTJ48+YaZGjZsaISEhBg2m825bMGCBQZgfP755859Jicnp9vuwoULRrFixYzHHnss3XLAePPNN52vJ0+ebABGVFSUYRiGcfr0acPd3d245557DLvd7lzv1VdfNQCjT58+zmVJSUnpchmG47v28PBI99ls3Ljxmuf735+VK5/Z22+/nW69Bx54wLBYLOl+BjL7c3EtKSkpRkBAgPHaa685lz3yyCNG7dq10633559/GoDxzDPPZNjHlc9o//79houLi9G1a9cMn8m/P8f/fv5XlC1bNt1ne+V7ufPOO420tLR0617t53Tt2rUGYEydOtW5bMSIEQZgzJkz55q5Fy5caADGH3/8ke79WrVqGS1btsywnYiISG6n69sbn5+ubx3y2/XtlZ/JsWPHXnOdcePGGYAxbdo057KUlBSjSZMmho+PjxEXF2cYhmE8++yzhp+fX4br0H+rXbu2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IRMmTADAbrdTunRpnn76aV5++eUbbj9u3DhGjBjByZMn8fb2zu64IiIiIiIiIiIikkmmjvmYkpLC5s2beeWVV5zLXFxcCA8PZ+3atZnax9dff02PHj2uWXhMTk4mOTnZ+dput3P+/HkCAgKwWCy3dwIiIiIiJjAMg4sXL1KyZElcXEzvyCK3wG63c+LECXx9fXVNKiIiInnOzVyPmlp8PHv2LDabjWLFiqVbXqxYMfbu3XvD7Tds2MDOnTv5+uuvr7nOmDFjGDVq1G1nFREREcltjh49SkhIiNkx5BacOHGC0qVLmx1DRERE5LZk5no0T892/fXXX1OzZs1rTk4D8MorrzBs2DDn69jYWMqUKcPRo0fx8/PLiZgiIiIiWSouLo7SpUvj6+trdhS5RVe+O12TioiISF50M9ejphYfAwMDsVqtnDp1Kt3yU6dOUbx48etum5CQwIwZMxg9evR11/Pw8MDDwyPDcj8/P13oiYiISJ6m7rp515XvTtekIiIikpdl5nrU1EGC3N3dqV+/PkuXLnUus9vtLF26lCZNmlx321mzZpGcnMyjjz6a3TFFRERERERERETkFpje7XrYsGH06dOHBg0a0KhRI8aNG0dCQgL9+vUDoHfv3pQqVYoxY8ak2+7rr7+mS5cuBAQEmBFbREREREREREREbsD04uNDDz3EmTNnGDFiBNHR0dSpU4cFCxY4J6E5cuRIhllz9u3bx+rVq1m0aJEZkUVERERERERERCQTLIZhGGaHyElxcXH4+/sTGxur8XVEREQkT9L1TN6n71BERLKKYRikpaVhs9nMjiL5jJubG1ar9arv3cy1jOktH0VERERERERE5OalpKRw8uRJEhMTzY4i+ZDFYiEkJAQfH5/b2o+KjyIiIiIiIiIieYzdbicqKgqr1UrJkiVxd3fP1MzDIplhGAZnzpzh2LFjVKxY8ZotIDNDxUcRERERERERkTwmJSUFu91O6dKl8fLyMjuO5ENBQUEcOnSI1NTU2yo+utx4FRERERERERERyY3+O0mvSFbJqpa0+gkVERERERERERGRbKHio4iIiIiIiIiIiGQLFR9FRERERERERCTPKleuHOPGjcv0+suXL8disRATE5NtmeQfKj6KiIiIiIiIiEi2s1gs132MHDnylva7ceNGHn/88Uyv37RpU06ePIm/v/8tHS+zVOR0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ClBsbGzOx/vvv6+goKBcjz355JM55zocDmVk5G0Wa9myZa+o+Y63t7dCQ0MvvJ9gQBnrNu2UtYS5ACxcuFCnT5/WXXfdpc8++6xAnvOi0rOLjxdvNkPzFgAAADg7Lw+7Prq3mSqW8tPuY8kaPG2NMjKzTMfKN4qPAOAKIgdIdi9p31LpwGrTafJv/0pp/wrJw/tsQTUPHA6HktMyjHzktQtdaGhozkdwcLBsNlvO/c2bNyswMFC//PKLmjdvLh8fHy1cuFA7duzQbbfdpvLly6tEiRJq0aKFfvvtt1zP++9l1zabTZ9++qm6du0qf39/1apVSz/88EPO5/+97HrKlCkqWbKkfv31V9Vr1EQlarfVTfc+otgdG3K+JiMjQ4899phKliyp0qVLa9iwYerbt69uv/32y77viRMn6p577lHv3r01adKk8z6/f/9+9ezZUyEhIQoICFBkZKSWLVuW8/kff/xRLVq0kK+vr8qUKaOuXbvmeq+zZ8+27mRlSBmpKlnvWk2Z9o0kaffu3bLZbJoxY4batWsnX19fffnllzp27Jh69uypChUqyN/fX40aNdJXX32VK1dWVpbefPNN1axZUz4+PqpcubJee+01SdL111+vwYMH5zr/yJEj8vb21vz58y97TQAAAIDLKV3CRxP6RMrf20MLtx/VyJ83m46Ub56mAwAACkBQmNTwDmndDGnZeOmOT0wnyp/sWY8N75ICy+f5y06nZ6r+iF8LKdSlbXy5o/y9C+Z/p88884zefvttVa9eXaVKldK+fft0880367XXXpOPj48+//xzdenSRVu2bFHlypUv+jwvvfSS3nzzTb311lv68MMPde+992rPnj0KCQm54PnJycl6++23NXXqVNkzUtSrTx89+d8X9OXXP0gennrjjTf05ZdfavLkyapXr55Gjx6t2bNn67rrrrvk+zl16pS+/vprLVu2THXr1lV8fLz+/vtvXXPNNZKkxMREtWvXThUqVNAPP/yg0NBQrV69WllZ1l9158yZo65du+rZZ5/V559/rrS0NP38888XfrG0M/s9ymYtIf/XdX3nnXfUtGlT+fr6KiUlRc2bN9ewYcMUFBSkOXPmqHfv3qpRo4aioqIkScOHD9eECRP03nvvqW3btoqNjdXmzdaAb+DAgRo8eLDeeecd+fhYs3O/+OILVahQQddff/0lrwkA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KEXhS32vM54p/vg3BAAAV+O/363XtGV7Fejjqe8eaa2a5QKL9PWvZCzDzEcAcEXZTVs2z5GO7zKb5VKO7ZC2zrWO89FoBoXM21/yLqE9+w9owtjR2rp1q9avX6+HHnpIu3bt0j333GM6oZSVaRUeJWv2bBFIT09XXFycnnvuObVs2bJoZ6MCAAAAkl7s0kBRVUN0KjVDAz9bqfjkdNORLoriIwC4orJ1pJodJDmk5Z+YTnNxyz6W5JBqdZTK1DSdBhcSUFZ2m11Tpk5TixYt1KZNG61fv16//fab6tWrZzrd2cKj3UvyuPx+jwVh0aJFCgsL04oVKzR+/PgieU0AAADgXN6edo3r1UwVSvpp97FkDf5qtTIyi3J/+Lyj+AgArir6Iet29VQpJcFslgtJiZdiziwJb8msR6flG6xKlStr0feTFH9whxISErR48WJde+21ppNZ0pOsW29/6SINcApa+/bt5XA4tGXLFjVq1KhIXhP599dff6lLly4KDw+XzWbT7NmzL/s1CxYsULNmzeTj46OaNWtqypQp550zduxYVa1aVb6+voqOjs61HykAAEBRKF3CRxP6RMrPy0N/bzuq13/ZbDrSBTlF8fFKB29ff/216tatK19fXzVq1Eg///xzESUFgGKkxvVSmdpS2ikpZprpNOdb84WUliiVrStVv850GlyMzSYFlLWOk444Xwf1tDPFxyJaco3iJykpSRERERo7dmyezt+1a5c6d+6s6667TjExMXriiSc0cOBA/frrrznnzJgxQ0OHDtULL7yg1atXKyIiQh07djyvKREAAEBhqx8epHe6R0iSPl24S9+s2m840fmMFx+vdPC2ePFi9ezZUwMGDNCaNWt0++236/bbb9eGDRuKODkAODm7XYp+wDpeNl7KcqIp+FmZZ5Zcy9rrsYhmrCGf/EMkm13KSLEKxs4kLdm69ab4iAvr1KmTXn311Qt2X7+Q8ePHq1q1anrnnXdUr149DR48WHfddZfee++9nHPeffddDRo0SP3791f9+vU1fvx4+fv7a9KkSYX1NgAAAC7q5kZheux6axur/367Xqv3njCcKDdP0wHOHbxJ1oBvzpw5mjRpkp555pnzzh89erRuuukmPfXUU5KkV155RfPmzdOYMWPYdwkA/i2ipzT/ZenELmnhO1KZOqYTWY5skU7usToTN+5hOg0u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AABAcUTxEQCAItS9e3fZ7XZNmzZNn3/+ue67776c/R8XLVqk2267Tb169VJERISqV6+urVu35vm569Wrp3379uVq1LZ06dJc5yxevFhVqlTRs88+q8jISNWqVUt79uzJdY63t7cyMzMv+1pr165VUlJSzmOLFi2S3W5XnTp18pz53yZOnKi7775bMTExuT7uvvvunMYzjRs31t9//33BomFgYKCqVq2aU6j8t+zu4Odeo3Obz1zKokWL1K9fP3Xt2lWNGjVSaGiodu/enfP5Ro0aKSsrS3/++edFn+Pmm29WQECAxo0bp7lz5+q+++7L02sDAAAAxRXFRwAAilCJEiXUo0cPDR8+XLGxsbm66NaqVUvz5s3T4sWLtWnTJj3wwAM6dOhQnp+7Q4cOql27tvr27au1a9fq77//1rPPPpvrnFq1amnv3r2aPn26duzYoQ8++EDfffddrnOqVq2qXbt2KSYmRkePHlVqaup5r3XvvffK19dXffv21YYNG/THH3/o0UcfVe/evXOWXF+pI0eO6Mcff1Tfvn3VsGHDXB99+vTR7Nmzdfz4cQ0ePFgJCQm6++67tXLlSm3btk1Tp07Vli1bJEkvvvii3nnnHX3wwQfatm2bVq9erQ8//FCSNTuxZcuWev3117Vp0yb9+eefufbAvJRatWrp22+/VUxMjNauXat77rkn1yzOqlWrqm/fvrrvvvs0e/Zs7dq1SwsWLNDMmTNzzvHw8FC/fv00fPhw1apV64LL4gEAAABXQvERAIAiNmDAAJ04cUIdO3bMtT/jc889p2bNmqljx45q3769QkNDdfvtt+f5ee12u7777judPn1aUVFRGjhwoF577bVc59x6660aMmSIBg8erCZNmmjx4sV6/vnnc51z55136qabbtJ1112nsmXL6quvvjrvtfz9/fXrr7/q+PHjatGihe666y7dcMMNGjNmzJVdjHNkN6+50H6NN9xwg/z8/PTFF1+odOnS+v3335WYmKh27dqpefPmmjBhQs4S7759++r999/XRx99pAYNGuiWW27Rtm3bcp5r0qRJysjIUPPmzfXEE0/o1VdfzVO+d999V6VKlVLr1q3VpUsXdezYUc2aNct1zrhx43TXXXfp4YcfVt26dTVo0KBcs0Ml698/LS1N/fv3v9JLBAAAABQ7Nse5mx65gYSEBAUHBys+Pv6KN9cHAJiXkpKiXbt2qVq1avL19TUdB7hif//9t2644Qbt27fvkrNEL/W9znim+OPfEAAAFGdXMpah2zUAAEARSE1N1ZEjR/Tiiy+qW7du+V6eDgAAABQnLLsGAAAoAl999ZWqVKmikydP6s033zQdBwAAACgSFB8BAACKQL9+/ZSZmalVq1apQoUKpuMAAAAARYLiIwAAAAAAAIBCQfERAFAsuVm/NLghvscBAADgCig+AgCKFS8vL0lScnKy4SRA4cr+Hs/+ngcAAACKI7pdAwCKFQ8PD5UsWVKHDx+WJPn7+8tmsxlOBRQch8Oh5ORkHT58WCVLlpSHh4fpSAAAAEC+UXwEABQ7oaGhkpRTgARcUcmSJXO+1wEAAIDiiuIjAKDYsdlsCgsLU7ly5ZSenm46DlDgvLy8mPEIAAAAl0DxEQBQbHl4eFCgAQAAAAAnRsMZAAAAAAAAAIWC4iMAAAAAAACAQkHxEQAAAAAAAEChcLs9Hx0OhyQpISHBcBIAAID8yR7HZI9rUPwwJgUAAMXZlYxH3a74eOrUKUlSpUqVDCcBAAC4OqdOnVJwcLDpGMgHxqQAAMAV5GU8anO42Z/Ms7KydPDgQQUGBspmsxXa6yQkJKhSpUrat2+fgoKCCu11ijOu0eVxjS6Pa5Q3XKfL4xpdHtfo8orqGjkcDp06dUrh4eGy29lFpzgqijEp/81eHtcob7hOl8c1ujyu0eVxjS6Pa5Q3RXGdrmQ86nYzH+12uypWrFhkrxcUFMR/EJfBNbo8rtHlcY3yhut0eVyjy+MaXV5RXCNmPBZvRTkm5b/Zy+Ma5Q3X6fK4RpfHNbo8rtHlcY3yprCvU17Ho/ypHAAAAAAAAEChoPgIAAAAAAAAoFBQfCwkPj4+euGFF+Tj42M6itPiGl0e1+jyuEZ5w3W6PK7R5XGNLo9rBGfC9+PlcY3yhut0eVyjy+MaXR7X6PK4RnnjbNfJ7RrOAAAAAAAAACgazHwEAAAAAAAAUCgoPgIAAAAAAAAoFBQfAQAAAAAAABQKio8AAAAAAAAACgXFx0IwduxYVa1aVb6+voqOjtby5ctNR3Iqo0aNUosWLRQYGKhy5crp9ttv15YtW0zHcmqvv/66bDabnnjiCdNRnMqBAwfUq1cvlS5dWn5+fmrUqJFWrlxpOpbTyMzM1PPPP69q1arJz89PNWrU0CuvvCJ37zP2119/qUuXLgoPD5fNZtPs2bNzfd7hcGjEiBEKCwuTn5+fOnTooG3btpkJa8ilrlF6erqGDRumRo0aKSAgQOHh4erTp48OHjxoLrABl/s+OteDDz4om82m999/v8jyARJj0kthPHrlGI9eGOPRy2NMej7Go5fHePTyitN4lOJjAZsxY4aGDh2qF154QatXr1ZERIQ6duyow4cPm47mNP7880898sgjWrp0qebNm6f09HT93//9n5KSkkxHc0orVqzQxx9/rMaNG5uO4lROnDihNm3ayMvLS7/88os2btyod955R6VKlTIdzWm88cYbGjdunMaMGaNNmzbpjTfe0JtvvqkPP/zQdDSjkpKSFBERobFjx17w82+++aY++OADjR8/XsuWLVNAQIA6duyolJSUIk5qzqWuUXJyslavXq3nn39eq1ev1rfffqstW7bo1ltvNZDUnMt9H2X77rvvtHTpUoWHhxdRMsDCmPTSGI9eGcajF8Z4NG8Yk56P8ejlMR69vGI1HnWgQEVFRTkeeeSRnPuZmZmO8PBwx6hRowymcm6HDx92SHL8+eefpqM4nVOnTjlq1arlmDdvnqNdu3aOxx9/3HQkpzFs2DBH27ZtTcdwap07d3bcd999uR674447HPfee6+hRM5HkuO7777LuZ+VleUIDQ11vPXWWzmPnTx50uHj4+P46quvDCQ079/X6EKWL1/ukOTYs2dP0YRyMhe7Rvv373dUqFDBsWHDBkeVKlUc7733XpFng/tiTHplGI9eHOPRi2M8mjeMSS+N8ejlMR69PGcfjzLzsQClpaVp1apV6tChQ85jdrtdHTp00JIlSwwmc27x8fGSpJCQEMNJnM8jjzyizp075/qeguWHH35QZGSkunXrpnLlyqlp06aaMGGC6VhOpXXr1po/f762bt0qSVq7dq0WLlyoTp06GU7mvHbt2qW4uLhc/80FBwcrOjqan+OXEB8fL5vNppIlS5qO4jSysrLUu3dvPfXUU2rQoIHpOHAzjEmvHOPRi2M8enGMR/OGMemVYTyaP4xHz+dM41FPo6/uYo4eParMzEyVL18+1+Ply5fX5s2bDaVybllZWXriiSfUpk0bNWzY0HQcpzJ9+nStXr1aK1asMB3FKe3cuVPjxo3T0KFD9d///lcrVqzQY489Jm9vb/Xt29d0PKfwzDPPKCEh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",
            "text/plain": [
              "<Figure size 1600x800 with 2 Axes>"
            ]
          },
          "metadata": {},
          "output_type": "display_data"
        }
      ],
      "source": [
        "# Learning curves \n",
        "\n",
        "acc = history.history['accuracy']\n",
        "val_acc = history.history['val_accuracy']\n",
        "loss=history.history['loss']\n",
        "val_loss=history.history['val_loss']\n",
        "\n",
        "plt.figure(figsize=(16,8))\n",
        "plt.subplot(1, 2, 1)\n",
        "plt.plot(acc, label='Training Accuracy')\n",
        "plt.plot(val_acc, label='Validation Accuracy')\n",
        "plt.legend(loc='lower right')\n",
        "plt.title('Training and Validation Accuracy')\n",
        "plt.xlabel(\"epochs\")\n",
        "plt.ylabel(\"accuracy\")\n",
        "\n",
        "plt.subplot(1, 2, 2)\n",
        "plt.plot(loss, label='Training Loss')\n",
        "plt.plot(val_loss, label='Validation Loss')\n",
        "plt.legend(loc='upper right')\n",
        "plt.title('Training and Validation Loss')\n",
        "plt.xlabel(\"epochs\")\n",
        "plt.ylabel(\"loss\")\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "YJ2romsAsshs"
      },
      "source": [
        "## BiLSTM\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 75,
      "metadata": {
        "id": "b02HsFGVs0WV"
      },
      "outputs": [],
      "source": [
        "def define_model3(vocab_size, max_length):\n",
        "    model3 = Sequential()\n",
        "    model3.add(Embedding(vocab_size,300, input_length=max_length))\n",
        "    model3.add(Bidirectional(LSTM(500)))\n",
        "    model3.add(Dense(10, activation='softmax'))\n",
        "    \n",
        "    model3.compile(loss = 'categorical_crossentropy',optimizer = 'adam',metrics = ['accuracy'])\n",
        "    \n",
        "    # summarize defined model\n",
        "    model3.summary()\n",
        "    return model3"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 76,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "I4VV9MlFs1Va",
        "outputId": "2c1f7a8a-5f09-4d3c-aa1d-86adb03de019"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Model: \"sequential_4\"\n",
            "_________________________________________________________________\n",
            " Layer (type)                Output Shape              Param #   \n",
            "=================================================================\n",
            " embedding_4 (Embedding)     (None, 10, 300)           19800     \n",
            "                                                                 \n",
            " bidirectional (Bidirection  (None, 1000)              3204000   \n",
            " al)                                                             \n",
            "                                                                 \n",
            " dense_5 (Dense)             (None, 10)                10010     \n",
            "                                                                 \n",
            "=================================================================\n",
            "Total params: 3233810 (12.34 MB)\n",
            "Trainable params: 3233810 (12.34 MB)\n",
            "Non-trainable params: 0 (0.00 Byte)\n",
            "_________________________________________________________________\n"
          ]
        }
      ],
      "source": [
        "model3 = define_model3(vocab_size, max_length)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 77,
      "metadata": {},
      "outputs": [
        {
          "data": {
            "text/plain": [
              "(12, 10)"
            ]
          },
          "execution_count": 77,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "X_train.shape"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 78,
      "metadata": {},
      "outputs": [
        {
          "data": {
            "text/plain": [
              "(12, 10)"
            ]
          },
          "execution_count": 78,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "y_train.shape"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 79,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "xfNlWQazs1Sa",
        "outputId": "34d4b707-9efd-4f6f-de1c-af46e0b2950a"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Epoch 1/10\n",
            "1/1 [==============================] - 2s 2s/step - loss: 2.3005 - accuracy: 0.0833 - val_loss: 2.2893 - val_accuracy: 0.0000e+00\n",
            "Epoch 2/10\n",
            "1/1 [==============================] - 0s 62ms/step - loss: 2.2313 - accuracy: 0.5000 - val_loss: 2.2789 - val_accuracy: 0.0000e+00\n",
            "Epoch 3/10\n",
            "1/1 [==============================] - 0s 64ms/step - loss: 2.1576 - accuracy: 0.5000 - val_loss: 2.2729 - val_accuracy: 0.0000e+00\n",
            "Epoch 4/10\n",
            "1/1 [==============================] - 0s 67ms/step - loss: 2.0696 - accuracy: 0.5000 - val_loss: 2.2836 - val_accuracy: 0.1000\n",
            "Epoch 5/10\n",
            "1/1 [==============================] - 0s 70ms/step - loss: 1.9613 - accuracy: 0.5000 - val_loss: 2.3534 - val_accuracy: 0.1000\n",
            "Epoch 6/10\n",
            "1/1 [==============================] - 0s 75ms/step - loss: 1.8449 - accuracy: 0.5000 - val_loss: 2.5315 - val_accuracy: 0.1000\n",
            "Epoch 7/10\n",
            "1/1 [==============================] - 0s 81ms/step - loss: 1.7580 - accuracy: 0.5000 - val_loss: 2.5346 - val_accuracy: 0.1000\n",
            "Epoch 8/10\n",
            "1/1 [==============================] - 0s 68ms/step - loss: 1.6176 - accuracy: 0.5000 - val_loss: 2.4349 - val_accuracy: 0.1000\n",
            "Epoch 9/10\n",
            "1/1 [==============================] - 0s 69ms/step - loss: 1.4490 - accuracy: 0.5833 - val_loss: 2.3535 - val_accuracy: 0.1000\n",
            "Epoch 10/10\n",
            "1/1 [==============================] - 0s 71ms/step - loss: 1.2853 - accuracy: 0.9167 - val_loss: 2.3171 - val_accuracy: 0.1000\n"
          ]
        }
      ],
      "source": [
        "history = model3.fit(X_train, y_train, epochs=10, verbose=1,validation_data=(X_test,y_test))"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 80,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 513
        },
        "id": "_XGvXqCfs1Qf",
        "outputId": "45e3d1d9-1171-4f92-9a6e-53c29ff8583e"
      },
      "outputs": [
        {
          "data": {
            "image/png": "iVBORw0KGgoAAAANSUhEUgAABR8AAAK9CAYAAACtshu3AAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8WgzjOAAAACXBIWXMAAA9hAAAPYQGoP6dpAADjy0lEQVR4nOzdd3QU5dvG8e9m0yuQhN5D6L0pIE2RpkgTEZEmoFJUUBR5URT0BxasoIAgoCKCUi30jvRepPdekpCEJKTtzvvHwkqkBUiYlOtzzhx3Zmdmr92s8HDnKRbDMAxERERERERERERE0piL2QFEREREREREREQka1LxUURERERERERERNKFio8iIiIiIiIiIiKSLlR8FBERERERERERkXSh4qOIiIiIiIiIiIikCxUfRUREREREREREJF2o+CgiIiIiIiIiIiLpQsVHERERERERERERSRcqPoqIiIiIiIiIiEi6UPFRJBPo2rUrRYsWvadr33//fSwWS9oGymCOHTuGxWJh8uTJD/y1LRYL77//vnN/8uTJWCwWjh07dsdrixYtSteuXdM0z/18V0REREQeFLVvb0/t23+pfSuS+an4KHIfLBZLqrYVK1aYHTXbe/XVV7FYLBw6dOiW5wwePBiLxcLOnTsfYLK7d+bMGd5//322b99udpSb2rt3LxaLBU9PTyIjI82OIyIiIndB7dvMQ+3b9HWtADxy5Eizo4hkeq5mBxDJzH766acU+z/++COLFy++4XiZMmXu63XGjx+P3W6/p2vfeecd3n777ft6/aygY8eOjBo1iqlTpzJkyJCbnvPLL79QoUIFKlaseM+v06lTJ5599lk8PDzu+R53cubMGYYOHUrRokWpXLlyiufu57uSVqZMmULevHm5dOkSM2bMoEePHqbmERERkdRT+zbzUPtWRDILFR9F7sPzzz+fYn/9+vUsXrz4huP/FRcXh7e3d6pfx83N7Z7yAbi6uuLqqv/VH3roIUqUKMEvv/xy08bZunXrOHr0KB999NF9vY7VasVqtd7XPe7H/XxX0oJhGEydOpXnnnuOo0eP8vPPP2fY4mNsbCw+Pj5mxxAREclQ1L7NPNS+FZHMQsOuRdJZgwYNKF++PFu2bKFevXp4e3vzf//3fwDMnTuXJ554gvz58+Ph4UFISAgffPABNpstxT3+O8/J9UMAvvvuO0JC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iGQFqWmPZrvio5+fH+D4cPz9/U1OIyIiInL3oqOjKVSokLNdI5mP2qQiIiKSmd1NezTbFR+vDWvx9/dXQ09EREQyNQ3XzbzUJhUREZGsIDXtUU0SJCIiIiIiIiIiIulCxUcRERERERERERFJFyo+ioiIiIiIiIiISLrIdnM+ioiIiIiIiIhkFYZhkJycjM1mMzuKZDFubm5Yrdb7vo+KjyIiIiIiIiIimVBiYiJnz54lLi7O7CiSBVksFgoWLIivr+993UfFRxERERERERGRTMZut3P06FGsViv58+fH3d09VSsPi6SGYRhcvHiRU6dOERoael89IFV8FBERERERERHJZBITE7Hb7RQqVAhvb2+z40gWFBwczLFjx0hKSrqv4qMWnBERERERERERyaRcXFTakfSRVj1p9Q0VERERERERERGRdKHio4iIiIiIiIiIiKQLFR9FRERERERERCTTKlq0KF9++WWqz1+xYgUWi4XIyMh0yyT/UvFRRERERERERETSncViue32/vvv39N9N23axIsvvpjq82vXrs3Zs2cJCAi4p9dLLRU5HbTatYiIiIiIiIiIpLuzZ886H0+fPp0hQ4awf/9+5zFfX1/nY8MwsNlsuLreuXQVHBx8Vznc3d3JmzfvXV0j9049H0VEREREREREMjnDMIhLTDZlMwwjVRnz5s3r3AICArBYLM79ffv24efnx/z586lWrRoeHh78/fffHD58mJYtW5InTx58fX2pUaMGS5YsSXHf/w67tlgsTJgwgdatW+Pt7U1oaCi///678/n/9kicPHkyOXLkYOHChZQpUwZfX1+aNm2aolianJzMq6++So4cOQgMDGTgwIF06dKFVq1a3fPP7NKlS3Tu3JmcOXPi7e1Ns2bNOHjwoPP548eP06JFC3LmzImPjw/lypVj3rx5zms7duxIcHAwXl5ehIaGMmnSpHvOkp7U81FEREREREREJJO7kmSj7JCFprz2nmFN8HZPmxLT22+/zciRIylevDg5c+bk5MmTNG/enP/97394eHjw448/0qJFC/bv30/hwoVveZ+hQ4fyySef8OmnnzJq1Cg6duzI8ePHyZUr103Pj4uLY+TIkfz000+4uLjw/PPPM2DAAH7++WcAPv74Y37++WcmTZpEmTJl+Oqrr5gzZw4NGza85/fatWtXDh48yO+//46/vz8DBw6kefPm7NmzBzc3N/r06UNiYiKrVq3Cx8eHPXv2OHuHvvvuu+zZs4f58+cTFBTEoUOHuHLlyj1nSU8qPoqIiIiIiIiISIYwbNgwHn/8ced+rly5qFSpknP/gw8+YPbs2fz+++/07dv3lvfp2rUrHTp0AGD48OF8/fXXbNy4kaZNm970/KSkJMaOHUtISAgAffv2ZdiwYc7nR40axaBBg2jdujUAo0ePdvZCvBfXio5r1qyhdu3aAPz8888UKlSIOXPm0K5dO06cOEHbtm2pUKECAMWLF3def+LECapUqUL16tUBR+/PjErFRxERERERERGRTM7LzcqeYU1Me+20cq2Ydk1MTAzvv/8+f/31F2fPniU5OZkrV65w4sSJ296nYsWKzsc+Pj74+/tz4cKFW57v7e3tLDwC5MuXz3l+VFQU58+fp2bNms7nrVYr1apVw26339X7u2bv3r24urry0EMPOY8FBgZSqlQp9u7dC8Crr75Kr169WLRoEY0aNaJt27bO99WrVy/atm3L1q1bady4Ma1atXIWMTMazfkoIiIiIiIiIpLJWSwWvN1dTdksFkuavQ8fH58U+wMGDGD27NkMHz6c1atXs337dipUqEBiYuJt7+Pm5nbD53O7QuHNzk/tXJbppUePHhw5coROnTqxa9cuqlevzqhRowBo1qwZx48fp3///pw5c4bHHnuMAQMGmJr3VlR8FBERERERERGRDGnNmjV07dqV1q1bU6FCBfLmzcuxY8ceaIaAgADy5MnDpk2bnMdsNhtbt26953uWKVOG5ORkNmzY4DwWHh7O/v37KVu2rPNYoUKFePnll5k1axZvvPEG48ePdz4XHBxMly5dmDJlCl9++SXffffdPedJTxp2LSIiIiIiIiIiGVJoaCizZs2iRYsWWCwW3n333Xse6nw/XnnlFUaMGEGJEiUoXbo0o0aN4tKlS6nq9blr1y78/Pyc+xaLhUqVKtGyZUt69uzJuHHj8PPz4+2336ZAgQK0bNkSgH79+tGsWTNKlizJpUuXWL58OWXKlAFgyJAhVKtWjXLlypGQkMCff/7pfC6jUfFRREREREREREQypM8//5wXXniB2rVrExQUxMCBA4mOjn7gOQYOHMi5c+fo3LkzVquVF198kSZNmmC13nm+y3r16qXYt1qtJCcnM2nSJF577TWefPJJEhMTqVev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aZ555hktXLhQo0aN0vbt2zV06FCtW7dOffv2NfUjAADwrx566CEtWrRIhw8f/sdjU6ZMUePGjdWoUaOrft1SpUrJz88vPyL+q7Jly8rb27tQ3mvevHmqX7++6tSpY3y1pcPhUHZ2ttEMAAAAgKsyXj526tRJI0eO1JAhQxQZGam4uDgtXLjQuanMwYMHdezYMefxLVq00IwZM/TJJ58oIiJCX3zxhRYsWKAGDRqY+hEAAKY5HFJmmpmbw3FFEe+66y6VKlVKU6dOzXV/amqq5s6dq4ceekinTp1Sly5dVKFCBfn5+alhw4aaOXPmZV/375dd79q1SzfccIN8fHxUr149LVq06B/PGThwoGrVqiU/Pz9Vq1ZNr776qrKysiRJU6dO1euvv66NGzfKYrHIYrE4M//9sutNmzbplltuka+vr0qWLKlHH31Uqampzsd79eql9u3ba+TIkSpXrpxKliypp556yvlelzNp0iR1795d3bt316RJk/7x+JYtW3TXXXcpKChIgYGBatWqlfbs2eN8fPLkyapfv768vb1Vrlw55z9S7t+/XxaLRXFxcc5jExMTZbFYtGTJEknSkiVLZLFY9MMPPygmJkbe3t5asWKF9uzZo3vuuUdlypRRQECAmjRpop9//jlXroyMDA0cOFDh4eHy9vZWjRo1NGnSJDkcDtWoUUMjR47MdXxcXJwsFot27979r78TAAAAwBUViQ1n+vbte8mVixf+H4G/euCBB/TAAw8UcCoAgMvISpfeLm/mvV86Knn5/+thHh4e6tGjh6ZOnaqXX35ZFotFkjR37lzl5OSoS5cuSk1NVUxMjAYOHKigoCB99913evDBB1W9enU1bdr0X9/DbrfrvvvuU5kyZbR69WolJSXlmg95QWBgoKZOnary5ctr06ZNeuSRRxQYGKgXX3xRnTp10ubNm7Vw4UJnsRYcHPyP10hLS1ObNm3UvHlzrV27VgkJCXr44YfVt2/fXAXrr7/+qnLlyunXX3/V7t271alTJ0VGRuqRRx655M+xZ88erVq1Sl9++aUcDoeee+45HThwQJUrV5YkHTlyRDfccINuuukm/fLLLwoKCtLKlSudqxPHjx+v/v37a8SIEWrbtq2SkpK0cuXKf/39/d2gQYM0cuRIVatWTSVKlNChQ4d0xx136K233pK3t7emTZumdu3aaceOHapUqZKk81dsrFq1SmPGjFFERIT27dunkydPymKxqE+fPpoyZYoGDBjgfI8pU6bohhtuUI0aNa46HwAAAOAKikT5CABAcdCnTx+99957Wrp0qW666SZJ58un+++/X8HBwQoODs5VTD399NP68ccfNWfOnCsqH3/++Wdt375dP/74o8qXP1/Gvv322/+Y0/jKK684v65SpYoGDBigWbNm6cUXX5Svr68CAgLk4eFxyc3cJGnGjBk6d+6cpk2bJn//8+Xr2LFj1a5dO73zzjvOKxhKlCihsWPHymazqU6dOrrzzju1ePHiy5aPkydPVtu2bVWiRAlJUps2bTRlyhQNHTpUkjRu3DgFBwdr1qxZ8vT0lCTVqlXL+fw333xTzz//vJ555hnnfU2aNPnX39/fDRs2TLfddpvz+9DQUEVERDi/f+ONNzR//nx9/fXX6tu3r3bu3Kk5c+Zo0aJFat26tSSpWrVqzuN79eqlIUOGaM2aNWratKmysrI0Y8aMf6yGBAAAANwJ5SMAwPV5+p1fgWjqva9QnTp11KJFC02ePFk33XSTdu/ereXLl2vYsGGSpJycHL399tuaM2eOjhw5oszMTGVkZFzxTMdt27YpPDzcWTxKuuiGbLNnz9aYMWO0Z88epaamKjs7W0FBQVf8c1x4r4iICGfxKEktW7aU3W7Xjh07nOVj/fr1ZbP9b7e9cuXKadOmTZd83ZycHH366af64IMPnPd1795dAwYM0JAhQ2S1WhUXF6dWrVo5i8e/SkhI0NGjR3Xrrbde1c9zMY0bN871fWpqqoYOHarvvvtOx44dU3Z2ts6ePauDBw9KOn8Jtc1m04033njR1ytfvrzuvPNOTZ48WU2bNtU333yjjIwMruYAAACAWzM+8xEAgGtmsZy/9NnE7c/Lp6/UQw89pHnz5iklJUVTpkxR9erVnWXVe++9pw8++EADBw7Ur7/+qri4OLVp00aZmZn59qtatWqVunXrpjvuuEPffvutNmzYoJdffjlf3+Ov/l4QWiwW2e32Sx7/448/6siRI+rUqZM8PDzk4eGhzp0768CBA1q8eLEkydfX95LPv9xjkmS1nj/1cfxlVuelZlD+tViVpAEDBmj+/Pl6++23tXz5csXFxalhw4bO392/vbckPfzww5o1a5bOnj2rKVOmqFOnToW2YRAAAABgAuUjAACFqGPHjrJarZoxY4amTZumPn36OOc/rly5Uvfcc4+6d++uiIgIVatWTTt37rzi165bt64OHTqUa6O233//Pdcxv/32mypXrqyXX35ZjRs3Vs2aNXXgwIFcx3h5eSknJ+df32vjxo1KS0tz3rdy5UpZrVbVrl37ijP/3aRJk9S5c2fFxcXlunXu3Nm58UyjRo20fPnyi5aGgYGBqlKlirOo/LtSpUpJUq7f0V83n7mclStXqlevXrr33nvVsGFDlS1bVvv373c+3rBhQ9ntdi1duvSSr3HHHXfI399f48eP18KFC9WnT58rem8AAADAVVE+AgBQiAICAtSpUycNHjxYx44dU69evZyP1axZU4sWLdJvv/2mbdu26bHHHtPx48ev+LVbt26tWrVqqWfPntq4caOWL1+ul19+OdcxNWvW1MGDBzVr1izt2bNHY8aM0fz583MdU6VKFe3bt09xcXE6efKkMjIy/vFe3bp1k4+Pj3r27KnNmzfr119/1dNPP60HH3zQecn11Tpx4oS++eYb9ezZUw0aNMh169GjhxYsWKDTp0+rb9++Sk5OVufOnbVu3Trt2rVLn332mXbs2CFJGjp0qEaNGqUxY8Zo165dio2N1Ycffijp/OrE6667TiNGjNC2bdu0dOnSXDMwL6dmzZr68ssvFRcXp40bN6pr1665VnFWqVJFPXv2VJ8+fbRgwQLt27dPS5Ys0Zw5c5zH2Gw29erVS4MHD1bNmjUvelk8AAAA4E4oHwEAKGQPPfSQzpw5ozZt2uSaz/jKK68oOjpabdq00U033aSyZcuqffv2V/y6VqtV8+fP19mzZ9W0aVM9/PDDeuutt3Idc/fdd+u5555T3759FRkZqd9++02vvvpqrmPuv/9+3X777br55ptVqlQpzZw58x/v5efnpx9//FGnT59WkyZN1KFDB916660aO3bs1f0y/uLC5jUXm9d46623ytfXV59//rlKliypX375RampqbrxxhsVExOjiRMnOi/x7tmzp0aPHq2PPvpI9evX11133aVdu3Y5X2vy5MnKzs5WTEyMnn32Wb355ptXlO/9999XiRIl1KJFC7Vr105t2rRRdHR0rmPGjx+vDh066Mknn1SdOnX0yCOP5FodKp3//DMzM9W7d++r/RUBAAAALsfi+OvQo2IgOTlZwcHBSkpKuurh+gAA886dO6d9+/apatWq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cthsNtntdkOJAPfGOal74JzU9XE+6h44H3UPnI+axcrHfNa/f3/17NlTjRs3VtOmTTV69GilpaWpd+/epqPhCj311FOaMWOGvvrqKwUGBio+Pl6SFBwcLF9fX8PpcKUCAwP/MRPJ399fJUuWZFaSC3nuuefUokULvf322+rYsaPWrFmjTz75RJ988onpaLgK7dq101tvvaVKlSqpfv362rBhg95//3316dPHdDTAbXFO6vo4J3V9nI+6B85H3QPno2ZZHA6Hw3QIdzN27Fi99957io+PV2RkpMaMGaNmzZqZjoUrZLFYLnr/lClT1KtXr8INg3x10003KTIyUqNHjzYdBVfh22+/1eDBg7Vr1y5VrVpV/fv31yOPPGI6Fq5CSkqKXn31Vc2fP18JCQkqX768unTpoiFDhsjLy8t0PMBtcU7q2jgndU+cj7omzkddH+ejZlE+AgAAAAAAACgQzHwEAAAAAAAAUCAoHwEAAAAAAAAUCMpHAAAAAAAAAAWC8hEAAAAAAABAgaB8BAAAAAAAAFAgKB8BAAAAAAAAFAjKRwAAAAAAAAAFgvIRAAAAAAAAQIGgfAQAQ5YsWSKLxaLExETTUQAAAFBMcU4KoKBRPgIAAAAAAAAoEJSPAAAAAAAAAAoE5SOAYstut2v48OGqWrWqfH19FRERoS+++ELS/y4/+e6779SoUSP5+Pjouuuu0+bNm3O9xrx581S/fn15e3urSpUqGjVqVK7HMzIyNHDgQIWHh8vb21s1atTQpEmTch2zfv16NW7cWH5+fmrRooV27NjhfGzjxo26+eabFRgYqKCgIMXExGjdunUF9BsBAABAYeOcFIC7o3wEUGwNHz5c06ZN04QJE7RlyxY999xz6t69u5YuXeo85oUXXtCoUaO0du1alSpVSu3atVNWVpak8ydoHTt2VOfOnbVp0yYNHTpUr776qqZOnep8fo8ePTRz5kyNGTNG27Zt08cff6yAgIBcOV5++WWNGjVK69atk4eHh/r06eN8rFu3bqpYsaLWrl2r9evXa9CgQfL09CzYXwwAAAAKDeekANydxeFwOEyHAIDClpGRodDQUP38889q3ry58/6HH35Y6enpevTRR3XzzTdr1qxZ6tSpkyTp9OnTqlixoqZOnaqOHTuqW7duOnHihH766Sfn81988UV999132rJli3bu3KnatWtr0aJFat269T8yLFmyRDfffLN+/vln3XrrrZKk77//XnfeeafOnj0rHx8fBQUF6cMPP1TPnj0L+DcCAACAwsY5KYDigJWPAIql3bt3Kz09XbfddpsCAgKct2nTpmnPnj3O4/56EhgaGqratWtr27ZtkqRt27apZcuWuV63ZcuW2rVrl3JychQXFyebzaYbb7zxslkaNWrk/LpcuXKSpISEBElS//799fDDD6t169YaMWJErmwAAABwbZyTAigOKB8BFEupqamSpO+++05xcXHO29atW50zdq6Vr6/vFR3310tWLBaLpPOzfyRp6NCh2rJli+6880798ssvqlevnubPn58v+QAAAGAW56QAigPKRwDFUr169eTt7a2DBw+qRo0auW7h4eHO437//Xfn12fOnNHOnTtVt25dSVLdunW1cuXKXK+7cuVK1apVSzabTQ0bNpTdbs81rycvatWqpeeee04//fST7rvvPk2ZMuWaXg8AAABFA+ekAIoDD9MBAMCEwMBADRgwQM8995zsdruuv/56JSUlaeXKlQoKClLlypUlScOGDVPJkiVVpkwZvfzyywoLC1P79u0lSc8//7yaNGmiN954Q506ddKqVas0duxYffTRR5KkKlWqqGfPnurTp4/GjBmjiIgIHThwQAkJCerYseO/Zjx79qxeeOEFdejQQVWrVtXhw4e1du1a3X///QX2ewEAAEDh4ZwUQHFA+Qig2HrjjTdUqlQpDR8+XHv37lVISIiio6P10ksvOS8xGTFihJ555hnt2rVLkZGR+uabb+Tl5SVJio6O1pw5czRkyBC98cYbKleunIYNG6ZevXo532P8+PF66aWX9OSTT+rUqVOqVKmSXnrppSvKZ7PZdOrUKfXo0UPHjx9XWFiY7rvvPr3++uv5/rsAAACAGZyTAnB37HYNABdxYde/M2fOKCQkxHQcAAAAFEOckwJwB8x8BAAAAAAAAFAgKB8BAAAAAAAAFAguuwYAAAAAAABQIFj5CAAAAAAAAKBAUD4CAAAAAAAAKBCUjwAAAAAAAAAKBOUjAAAAAAAAgAJB+QgAAAAAAACgQFA+AgAAAAAAACgQlI8AAAAAAAAACgTlIwAAAAAAAIAC8f/uU9mCf8sQCgAAAABJRU5ErkJggg==",
            "text/plain": [
              "<Figure size 1600x800 with 2 Axes>"
            ]
          },
          "metadata": {},
          "output_type": "display_data"
        }
      ],
      "source": [
        "# Learning curves \n",
        "\n",
        "acc = history.history['accuracy']\n",
        "val_acc = history.history['val_accuracy']\n",
        "loss=history.history['loss']\n",
        "val_loss=history.history['val_loss']\n",
        "\n",
        "plt.figure(figsize=(16,8))\n",
        "plt.subplot(1, 2, 1)\n",
        "plt.plot(acc, label='Training Accuracy')\n",
        "plt.plot(val_acc, label='Validation Accuracy')\n",
        "plt.legend(loc='lower right')\n",
        "plt.title('Training and Validation Accuracy')\n",
        "plt.xlabel(\"epochs\")\n",
        "plt.ylabel(\"accuracy\")\n",
        "\n",
        "plt.subplot(1, 2, 2)\n",
        "plt.plot(loss, label='Training Loss')\n",
        "plt.plot(val_loss, label='Validation Loss')\n",
        "plt.legend(loc='upper right')\n",
        "plt.title('Training and Validation Loss')\n",
        "plt.xlabel(\"epochs\")\n",
        "plt.ylabel(\"loss\")\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "3I8Ykx3HGacK"
      },
      "source": [
        "Future scope -\n",
        "* embedding layer : GloVe\n",
        "* cross validation for testing\n",
        "* grid search CV"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "xL1vugJNLy5x"
      },
      "source": [
        "## Predictions"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 81,
      "metadata": {
        "id": "SnWEw7d5TcOv"
      },
      "outputs": [],
      "source": [
        "tf.get_logger().setLevel('ERROR')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 82,
      "metadata": {
        "id": "rnB6-nG6SelW"
      },
      "outputs": [],
      "source": [
        "def get_text(str_text):\n",
        "    # print(str_text)\n",
        "    input_text  = [str_text]\n",
        "    df_input = pd.DataFrame(input_text,columns=['questions'])\n",
        "    df_input\n",
        "    return df_input"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 83,
      "metadata": {
        "id": "1101EozZSefs"
      },
      "outputs": [],
      "source": [
        "model = model2\n",
        "tokenizer_t = joblib.load(path_to_dumps+'tokenizer_t.pkl')\n",
        "vocab = joblib.load(path_to_dumps+'vocab.pkl')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 84,
      "metadata": {
        "id": "c51lst4wSedH"
      },
      "outputs": [],
      "source": [
        "def tokenizer(entry):\n",
        "    tokens = entry.split()\n",
        "    re_punc = re.compile('[%s]' % re.escape(string.punctuation))\n",
        "    tokens = [re_punc.sub('', w) for w in tokens]\n",
        "    tokens = [word for word in tokens if word.isalpha()]\n",
        "    tokens = [lemmatizer.lemmatize(w.lower()) for w in tokens]\n",
        "    # stop_words = set(stopwords.words('english'))\n",
        "    # tokens = [w for w in tokens if not w in stop_words]\n",
        "    tokens = [word.lower() for word in tokens if len(word) > 1]\n",
        "    return tokens"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 85,
      "metadata": {
        "id": "FK79K154Sp4y"
      },
      "outputs": [],
      "source": [
        "def remove_stop_words_for_input(tokenizer,df,feature):\n",
        "    doc_without_stopwords = []\n",
        "    entry = df[feature][0]\n",
        "    tokens = tokenizer(entry)\n",
        "    doc_without_stopwords.append(' '.join(tokens))\n",
        "    df[feature] = doc_without_stopwords\n",
        "    return df"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 86,
      "metadata": {
        "id": "afJXXfckSp1u"
      },
      "outputs": [],
      "source": [
        "def encode_input_text(tokenizer_t,df,feature):\n",
        "    t = tokenizer_t\n",
        "    entry = entry = [df[feature][0]]\n",
        "    encoded = t.texts_to_sequences(entry)\n",
        "    padded = pad_sequences(encoded, maxlen=10, padding='post')\n",
        "    return padded"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 87,
      "metadata": {
        "id": "aVfxwXqFSpzc"
      },
      "outputs": [],
      "source": [
        "def get_pred(model,encoded_input):\n",
        "    pred = np.argmax(model.predict(encoded_input))\n",
        "    return pred"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 88,
      "metadata": {
        "id": "hoq7PSF6Sea4"
      },
      "outputs": [],
      "source": [
        "def bot_precausion(df_input,pred):\n",
        "    words = df_input.questions[0].split()\n",
        "    if len([w for w in words if w in vocab])==0 :\n",
        "        pred = 1\n",
        "    return pred"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 89,
      "metadata": {
        "id": "TVP1uNDjS1D2"
      },
      "outputs": [],
      "source": [
        "def get_response(df2,pred):\n",
        "    upper_bound = df2.groupby('labels').get_group(pred).shape[0]\n",
        "    r = np.random.randint(0,upper_bound)\n",
        "    responses = list(df2.groupby('labels').get_group(pred).response)\n",
        "    return responses[r]"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 90,
      "metadata": {
        "id": "AeKrDXvxS1A9"
      },
      "outputs": [],
      "source": [
        "def bot_response(response,):\n",
        "    print(response)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 91,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "7hLqCtf2Su8W",
        "outputId": "45fce787-be44-4006-96b2-0d3a1e2bc785"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "1/1 [==============================] - 0s 107ms/step\n",
            "Mental illnesses are health conditions that disrupt a person's thoughts, emotions, relationships, and daily functioning.\n"
          ]
        }
      ],
      "source": [
        "# wrong response\n",
        "\n",
        "df_input = get_text(\"What treatment options are available?\")\n",
        "\n",
        "#load artifacts \n",
        "tokenizer_t = joblib.load(path_to_dumps+'tokenizer_t.pkl')\n",
        "vocab = joblib.load('vocab.pkl')\n",
        "\n",
        "df_input = remove_stop_words_for_input(tokenizer,df_input,'questions')\n",
        "encoded_input = encode_input_text(tokenizer_t,df_input,'questions')\n",
        "\n",
        "pred = get_pred(model1,encoded_input)\n",
        "pred = bot_precausion(df_input,pred)\n",
        "\n",
        "response = get_response(df2,pred)\n",
        "bot_response(response)"
      ]
    }
  ],
  "metadata": {
    "colab": {
      "collapsed_sections": [],
      "name": "Retrieval based",
      "provenance": []
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