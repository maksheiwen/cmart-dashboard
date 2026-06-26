# ============================================================================
# UNIFIED TEXT ANALYTICS - VENDOR & CUSTOMER
# Sentiment Analysis + Topic Modeling
# For Cmart Changlun SULAM Project
# ============================================================================

# ============================================================================
# PYTHON 3.11+ COMPATIBILITY PATCH (for Malaya)
# ============================================================================
import inspect
from collections import namedtuple

if not hasattr(inspect, 'ArgSpec'):
    ArgSpec = namedtuple('ArgSpec', ['args', 'varargs', 'varkw', 'defaults'])
    inspect.ArgSpec = ArgSpec
    print("✅ Created inspect.ArgSpec")

if not hasattr(inspect, 'getargspec'):
    def getargspec(func):
        full = inspect.getfullargspec(func)
        return inspect.ArgSpec(full.args, full.varargs, full.varkw, full.defaults)
    inspect.getargspec = getargspec
    print("✅ Created inspect.getargspec")

print("✅ Patched inspect for Python 3.11+")

import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
import nltk
nltk.download('punkt', quiet=True)
from nltk.tokenize import sent_tokenize
import malaya

# ----------------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------------
DATA_FILES = {
    'vendor': 'data/vendor_transcript.txt',
    'customer': 'data/customers_transcripts.txt'
}
OUTPUT_BASE = 'outputs'

# Create output directories
os.makedirs(f'{OUTPUT_BASE}/vendor', exist_ok=True)
os.makedirs(f'{OUTPUT_BASE}/customer', exist_ok=True)

# ----------------------------------------------------------------------------
# STOPWORDS & PREPROCESSING FUNCTIONS (shared)
# ----------------------------------------------------------------------------
malay_stopwords = set("""
abdul abdullah acara ada adalah ahmad air akan akhbar akhir aktiviti alam amat amerika anak anggota antara antarabangsa apa apabila april as asas asean asia asing atas atau australia awal awam bagaimanapun bagi bahagian bahan baharu bahawa baik bandar bank banyak barangan baru baru-baru bawah beberapa bekas beliau belum berada berakhir berbanding berdasarkan berharap berikutan berjaya berjumlah berkaitan berkata berkenaan berlaku bermula bernama bernilai bersama berubah besar bhd bidang bilion bn boleh bukan bulan bursa cadangan china dagangan dalam dan dana dapat dari daripada dasar datang datuk demikian dengan depan derivatives dewan di diadakan dibuka dicatatkan dijangkakan diniagakan dis disember ditutup dolar dr dua dunia ekonomi eksekutif eksport empat enam faedah feb global hadapan hanya harga hari hasil hingga hubungan ia iaitu ialah indeks india indonesia industri ini islam isnin isu itu jabatan jalan jan jawatan jawatankuasa jepun jika jualan juga julai jumaat jumlah jun juta kadar kalangan kali kami kata katanya kaunter kawasan ke keadaan kecil kedua kedua-dua kedudukan kekal kementerian kemudahan kenaikan kenyataan kepada kepentingan keputusan kerajaan kerana kereta kerja kerjasama kes keselamatan keseluruhan kesihatan ketika ketua keuntungan kewangan khamis kini kira-kira kita klci klibor komposit kontrak kos kuala kuasa kukuh kumpulan lagi lain langkah laporan lebih lepas lima lot luar lumpur mac mahkamah mahu majlis makanan maklumat malam malaysia mana manakala masa masalah masih masing-masing masyarakat mata media mei melalui melihat memandangkan memastikan membantu membawa memberi memberikan membolehkan membuat mempunyai menambah menarik menawarkan mencapai mencatatkan mendapatkan menerima menerusi mengadakan mengambil mengenai menggalakkan menggunakan mengikut mengumumkan mengurangkan meningkat meningkatkan menjadi menjelang menokok menteri menunjukkan menurut menyaksikan menyediakan mereka merosot merupakan mesyuarat minat minggu minyak modal mohd mudah mungkin naik najib nasional negara negara-negara negeri niaga nilai nov ogos okt oleh operasi orang pada pagi paling pameran papan para paras parlimen parti pasaran pasukan pegawai pejabat pekerja pelabur pelaburan pelancongan pelanggan pelbagai peluang pembangunan pemberita pembinaan pemimpin pendapatan pendidikan penduduk penerbangan pengarah pengeluaran pengerusi pengguna pengurusan peniaga peningkatan penting peratus perdagangan perdana peringkat perjanjian perkara perkhidmatan perladangan perlu permintaan perniagaan persekutuan persidangan pertama pertubuhan pertumbuhan perusahaan peserta petang pihak pilihan pinjaman polis politik presiden prestasi produk program projek proses proton pukul pula pusat rabu rakan rakyat ramai rantau raya rendah ringgit rumah sabah sahaja saham sama sarawak satu sawit saya sdn sebagai sebahagian sebanyak sebarang sebelum sebelumnya sebuah secara sedang segi sehingga sejak sekarang sektor sekuriti selain selama selasa selatan selepas seluruh semakin semalam semasa sementara semua semula sen sendiri seorang sepanjang seperti sept september serantau seri serta sesi setiap setiausaha sidang singapura sini sistem sokongan sri sudah sukan suku sumber supaya susut syarikat syed tahap tahun tan tanah tanpa tawaran teknologi telah tempat tempatan tempoh tenaga tengah tentang terbaik terbang terbesar terbuka terdapat terhadap termasuk tersebut terus tetapi thailand tiada tidak tiga timbalan timur tindakan tinggi tun tunai turun turut umno unit untuk untung urus usaha utama walaupun wang wanita wilayah yang
""".split())

extra_stopwords = {
    'kalau', 'buat', 'lah', 'macam', 'jadi', 'saja', 'pun', 'ni', 'tu', 'kan',
    'je', 'nak', 'pergi', 'datang', 'ada', 'sana', 'sini', 'sebab', 'bila',
    'mana', 'kenapa', 'bagaimana', 'orang', 'kita', 'mereka', 'dia', 'saya',
    'awak', 'kamu', 'tak', 'tidak', 'bukan', 'ya', 'interview', 'kitaorang',
    'diorang', 'okay', 'oh', 'faham', 'jom', 'hmm', 'ah', 'bro', 'dekat',
    'sikit', 'tadi', 'ni', 'tu', 'lah', 'pun', 'nak', 'je', 'kan', 'saja',
    'kalau', 'macam', 'buat', 'jadi', 'baru', 'sana', 'sini', 'un', 'ses',
    'dll', 'takat', 'jelah', 'okey', 'dah', 'tau', 'jap', 'sikit', 'tadi',
    'ah', 'bro', 'macam', 'buat'
}
malay_stopwords = set([w.strip() for w in malay_stopwords])
malay_stopwords.update(extra_stopwords)

try:
    malaya_stopwords = malaya.text.function.get_stopwords()
    malay_stopwords.update(malaya_stopwords)
except:
    pass

try:
    stemmer = malaya.stem.sastrawi()
except:
    stemmer = malaya.stem.naive()

def tokenize_text(text):
    return re.findall(r'\b\w+\b', text)

def clean_and_stem(sentence):
    s = sentence.lower()
    s = re.sub(r'[^\w\s\']', ' ', s)
    tokens = tokenize_text(s)
    tokens = [t for t in tokens if t not in malay_stopwords and len(t) > 2]
    stemmed = [stemmer.stem(t) for t in tokens]
    return ' '.join(stemmed)

def clean_text_only(sentence):
    """Clean and remove stopwords, but DO NOT stem."""
    s = sentence.lower()
    s = re.sub(r'[^\w\s\']', ' ', s)
    tokens = tokenize_text(s)
    tokens = [t for t in tokens if t not in malay_stopwords and len(t) > 2]
    # No stemming! Return tokens as they are.
    return ' '.join(tokens)

def read_text_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

# ----------------------------------------------------------------------------
# PROCESS A SINGLE DATASET (Vendor or Customer)
# ----------------------------------------------------------------------------
def process_dataset(name, filepath, output_dir):
    print("\n" + "="*70)
    print(f"📊 PROCESSING: {name.upper()}")
    print("="*70)

    # ---------- LOAD ----------
    print(f"📖 Loading {name} text from {filepath}...")
    raw_text = read_text_file(filepath)
    print(f"✅ Loaded {len(raw_text)} characters.")

    # ---------- CLEAN ----------
    sentences = sent_tokenize(raw_text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    # Clean all sentences (for sentiment analysis)
    cleaned = [clean_and_stem(s) for s in sentences]
    cleaned = [c for c in cleaned if len(c.strip()) > 0]

    # Clean all sentences WITHOUT stemming (for topic modeling)
    cleaned_no_stem = [clean_text_only(s) for s in sentences]
    cleaned_no_stem = [c for c in cleaned_no_stem if len(c.strip()) > 0]
    print(f"📝 Total sentences: {len(sentences)}")

    cleaned = [clean_and_stem(s) for s in sentences]
    cleaned = [c for c in cleaned if len(c.strip()) > 0]
    print(f"🧹 After cleaning: {len(cleaned)} sentences")

    if cleaned:
        print("\n🔹 Sample cleaned sentence:")
        print(cleaned[0][:150] + "...")

    # ---------- SENTIMENT ----------
    print("\n" + "-"*50)
    print("📊 SENTIMENT ANALYSIS")
    print("-"*50)

    print("Loading sentiment model...")
    sentiment_model = malaya.sentiment.huggingface(
        model='mesolitica/sentiment-analysis-nanot5-small-malaysian-cased'
    )

    print("Predicting sentiments...")
    results = sentiment_model.predict(cleaned)

    positive = [s for s, lab in zip(cleaned, results) if lab == 'positive']
    negative = [s for s, lab in zip(cleaned, results) if lab == 'negative']
    neutral = [s for s, lab in zip(cleaned, results) if lab == 'neutral']

    print(f"Positive: {len(positive)}, Negative: {len(negative)}, Neutral: {len(neutral)}")

    # Save sentiment CSV
    sentiment_df = pd.DataFrame({
        'cleaned_sentence': cleaned,
        'sentiment': results
    })
    sentiment_df.to_csv(f'{output_dir}/sentiment_results.csv', index=False)
    print(f"✅ Sentiment CSV saved to {output_dir}/sentiment_results.csv")

    # Pie chart
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [len(positive), len(neutral), len(negative)]
    colors = ['#2ecc71', '#f1c40f', '#e74c3c']
    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title(f'{name.capitalize()} Sentiment Distribution')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/sentiment_pie.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Pie chart saved to {output_dir}/sentiment_pie.png")

    # Sentiment word clouds
    def save_wordcloud(texts, colormap, filename):
        if not texts:
            return
        wc = WordCloud(width=800, height=400, background_color='white', colormap=colormap)
        wc.generate(' '.join(texts))
        wc.to_file(f'{output_dir}/{filename}')
        print(f"✅ Wordcloud saved: {filename}")

    save_wordcloud(positive, "Greens", "wordcloud_positive.png")
    save_wordcloud(negative, "Reds", "wordcloud_negative.png")
    save_wordcloud(neutral, "Blues", "wordcloud_neutral.png")

    # Overall word cloud
    all_text = ' '.join(cleaned)
    wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis')
    wc.generate(all_text)
    wc.to_file(f'{output_dir}/wordcloud_{name}.png')
    print(f"✅ Overall wordcloud saved: {output_dir}/wordcloud_{name}.png")

    # ---------- TOPIC MODELING ----------
    print("\n" + "-"*50)
    print("📊 TOPIC MODELING (LDA vs NMF)")
    print("-"*50)

    if len(cleaned) < 10:
        print("⚠️ Too few sentences for topic modeling. Skipping.")
        return

    vectorizer = CountVectorizer(
        max_df=0.80,
        min_df=1,
        max_features=100,
        stop_words=list(malay_stopwords),
        ngram_range=(1, 2)
    )

    doc_term = vectorizer.fit_transform(cleaned_no_stem)
    feature_names = vectorizer.get_feature_names_out()

    bigrams = [f for f in feature_names if ' ' in f]
    print(f"Total features: {len(feature_names)} (bigrams: {len(bigrams)})")
    if bigrams:
        print("Sample bigrams:", bigrams[:5])

    def get_top_words(model, feature_names, n=8):
        topics = []
        for topic in model.components_:
            top_idx = topic.argsort()[-n:][::-1]
            top_words = [feature_names[i] for i in top_idx]
            topics.append(top_words)
        return topics

    print("Training LDA...")
    lda = LatentDirichletAllocation(n_components=3, random_state=42, max_iter=100)
    lda.fit(doc_term)
    lda_topics = get_top_words(lda, feature_names)

    print("Training NMF...")
    nmf = NMF(n_components=3, random_state=42, init='nndsvd')
    nmf.fit(doc_term)
    nmf_topics = get_top_words(nmf, feature_names)

    print("\nComparison Table (LDA vs NMF):")
    for i in range(3):
        print(f"\nTopic {i+1}:")
        print(f"  LDA: {', '.join(lda_topics[i])}")
        print(f"  NMF: {', '.join(nmf_topics[i])}")

    # Coherence score
    doc_freq = np.array(doc_term.sum(axis=0)).flatten()
    word_probs = doc_freq / doc_freq.sum()

    def coherence(topics, feature_names, word_probs):
        scores = []
        for topic in topics:
            score = sum(word_probs[np.where(feature_names == w)[0][0]] for w in topic if w in feature_names)
            scores.append(score / len(topic))
        return np.mean(scores)

    lda_coherence = coherence(lda_topics, feature_names, word_probs)
    nmf_coherence = coherence(nmf_topics, feature_names, word_probs)
    print(f"\nCoherence Score - LDA: {lda_coherence:.4f}")
    print(f"Coherence Score - NMF: {nmf_coherence:.4f}")

    best_model = lda
    best_topics = lda_topics
    best_name = "LDA"
    if nmf_coherence > lda_coherence:
        best_model = nmf
        best_topics = nmf_topics
        best_name = "NMF"

    print(f"\n✅ Best Model: {best_name}")

    # Save topics
    topics_df = pd.DataFrame({
        'topic_id': range(1, 4),
        'keywords': [' '.join(t) for t in best_topics]
    })
    topics_df.to_csv(f'{output_dir}/topics.csv', index=False)

    compare_df = pd.DataFrame({
        'Topic': [f'Topic {i+1}' for i in range(3)],
        'LDA Keywords': [', '.join(t) for t in lda_topics],
        'NMF Keywords': [', '.join(t) for t in nmf_topics]
    })
    compare_df.to_csv(f'{output_dir}/topic_model_comparison.csv', index=False)

    print(f"✅ Topics saved to {output_dir}/topics.csv")
    print(f"✅ Comparison saved to {output_dir}/topic_model_comparison.csv")

    # Bar chart
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for idx, topic_words in enumerate(best_topics):
        words = topic_words[:5]
        axes[idx].barh(words, range(len(words), 0, -1), color='skyblue')
        axes[idx].set_title(f'{best_name} Topic {idx+1}')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/topics_barchart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Bar chart saved to {output_dir}/topics_barchart.png")

    # Topic word clouds (with underscores)
    def generate_topic_wordclouds(topics_df, output_dir):
        for i, row in topics_df.iterrows():
            topic_id = row['topic_id']
            keywords = row['keywords']
            topic_words = keywords.split()
            cloud_text = ' '.join([w.replace(' ', '_') for w in topic_words])
            wc = WordCloud(width=400, height=300, background_color='white', colormap='viridis')
            wc.generate(cloud_text)
            wc.to_file(f'{output_dir}/topic_wordcloud_{topic_id}.png')
            print(f"✅ Topic wordcloud {topic_id} saved.")

    generate_topic_wordclouds(topics_df, output_dir)

    print(f"\n✅ {name.upper()} analysis complete!")
    print(f"All outputs saved to: {output_dir}/")

# ----------------------------------------------------------------------------
# RUN FOR BOTH VENDOR AND CUSTOMER
# ----------------------------------------------------------------------------
print("\n" + "="*70)
print("🚀 STARTING UNIFIED TEXT ANALYTICS")
print("="*70)

# Process Vendor
process_dataset('vendor', DATA_FILES['vendor'], f'{OUTPUT_BASE}/vendor')

# Process Customer
process_dataset('customer', DATA_FILES['customer'], f'{OUTPUT_BASE}/customer')

print("\n" + "="*70)
print("✅ ALL ANALYSIS COMPLETE!")
print("="*70)
print("\n📁 Outputs saved to:")
print("   outputs/vendor/  (vendor sentiment + topics)")
print("   outputs/customer/ (customer sentiment + topics)")
print("\n📌 Next: Run the dashboard:")
print("   cd dashboard")
print("   streamlit run app_streamlit.py")
print("="*70)