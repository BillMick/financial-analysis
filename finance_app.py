import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style

# Connexion à PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="analyse_des_ratios",
            user="postgres",
            password="",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Erreur de connexion", f"Erreur de connexion à la base de données : {e}")
        return None

# Ajouter nouvelles données 
def add_data():
    # Sauvegarde dans la base de données
    def save_to_db():
        # Eléments à sauvegarder
        postes = {
            "Année": int(annee_entry_2.get()),
            "Actif immobilisé": float(actif_entry_2.get()),
            "Actif circulant": float(circulant_entry_2.get()),
            "Total actif": float(total_actif_entry_2.get()),
            "Capitaux propres": float(capitaux_entry_2.get()),
            "Passif à long terme": float(long_term_entry_2.get()),
            "Passif circulant": float(circulant_passif_entry_2.get()),
            "Résultat net": float(resultat_net_entry_2.get()),
            "Chiffre d'affaires": float(chiffre_d_affaires_entry_2.get())
        }
        print(postes)
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS masses_bilan (
                        id SERIAL PRIMARY KEY,
                        annee INT NOT NULL UNIQUE,
                        actif_immobilise FLOAT,
                        actif_circulant FLOAT,
                        total_actif FLOAT,
                        capitaux_propres FLOAT,
                        passif_long_terme FLOAT,
                        passif_circulant FLOAT,
                        resultat_net FLOAT,
                        chiffre_d_affaire FLOAT
                    );
                """)
                cursor.execute("""
                    INSERT INTO masses_bilan (annee, actif_immobilise, actif_circulant, total_actif, capitaux_propres, passif_long_terme, passif_circulant, resultat_net, chiffre_d_affaire)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (postes["Année"], postes["Actif immobilisé"], postes["Actif circulant"], postes["Total actif"], postes["Capitaux propres"],
                    postes["Passif à long terme"], postes["Passif circulant"], postes["Résultat net"], postes["Chiffre d'affaires"]))
                conn.commit()
                messagebox.showinfo("Succès", "Données enregistrées avec succès dans la base de données.")
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement dans la base de données : {e}")
            finally:
                cursor.close()
                conn.close()
                top.withdraw()
                display_data()
    
    # Formulaire
    top = tk.Toplevel(root)
    top.title("Ajouter des données d'une année")
    top.geometry("320x380")
    
    # Champs pour saisie manuelle
    annee_label_2 = tk.Label(top, text="Année:", bg="#ffffff", font=("Times New Roman", 13))
    annee_label_2.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    annee_entry_2 = tk.Entry(top, font=("Times New Roman", 13), width=15)
    annee_entry_2.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    actif_label_2 = tk.Label(top, text="Actif immobilisé:", bg="#ffffff", font=("Times New Roman", 13))
    actif_label_2.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    actif_entry_2 = tk.Entry(top, font=("Times New Roman", 13), width=15)
    actif_entry_2.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    circulant_label_2 = tk.Label(top, text="Actif circulant:", bg="#ffffff", font=("Times New Roman", 13))
    circulant_label_2.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    circulant_entry_2 = tk.Entry(top, font=("Times New Roman", 13), width=15)
    circulant_entry_2.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    total_actif_label_2 = tk.Label(top, text="Total Actif:", bg="#ffffff", font=("Times New Roman", 13))
    total_actif_label_2.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    total_actif_entry_2 = tk.Entry(top, font=("Times New Roman", 13), width=15)
    total_actif_entry_2.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    capitaux_label_2 = tk.Label(top, text="Capitaux propres:", bg="#ffffff", font=("Times New Roman", 13))
    capitaux_label_2.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    capitaux_entry_2 = tk.Entry(top, font=("Times New Roman", 13), width=15)
    capitaux_entry_2.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    long_term_label_2 = tk.Label(top, text="Passif à long terme:", bg="#ffffff", font=("Times New Roman", 13))
    long_term_label_2.grid(row=5, column=0, padx=10, pady=5, sticky="e")
    long_term_entry_2 = tk.Entry(top, font=("Times New Roman", 13), width=15)
    long_term_entry_2.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    circulant_passif_label_2 = tk.Label(top, text="Passif circulant:", bg="#ffffff", font=("Times New Roman", 13))
    circulant_passif_label_2.grid(row=6, column=0, padx=10, pady=5, sticky="e")
    circulant_passif_entry_2 = tk.Entry(top, font=("Times New Roman", 13), width=15)
    circulant_passif_entry_2.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

    resultat_net_label_2 = tk.Label(top, text="Résultat net:", bg="#ffffff", font=("Times New Roman", 13))
    resultat_net_label_2.grid(row=7, column=0, padx=10, pady=5, sticky="e")
    resultat_net_entry_2 = tk.Entry(top, font=("Times New Roman", 13), width=15)
    resultat_net_entry_2.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

    chiffre_d_affaires_label_2 = tk.Label(top, text="Chiffre d'affaires:", bg="#ffffff", font=("Times New Roman", 13))
    chiffre_d_affaires_label_2.grid(row=8, column=0, padx=10, pady=5, sticky="e")
    chiffre_d_affaires_entry_2 = tk.Entry(top, font=("Times New Roman", 13), width=15)
    chiffre_d_affaires_entry_2.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

    separator = ttk.Separator(top, orient="horizontal")
    separator.grid(row=9, column=0, columnspan=2, pady=10, sticky="ew")

    save_button = ttk.Button(top, text="Enregistrer", command=save_to_db)
    save_button.grid(row=10, column=0, columnspan=2, pady=10)

    # top.withdraw()

# Charger les données de la base de données
def load_data():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS masses_bilan (
                        id SERIAL PRIMARY KEY,
                        annee INT NOT NULL UNIQUE,
                        actif_immobilise FLOAT,
                        actif_circulant FLOAT,
                        total_actif FLOAT,
                        capitaux_propres FLOAT,
                        passif_long_terme FLOAT,
                        passif_circulant FLOAT,
                        resultat_net FLOAT,
                        chiffre_d_affaire FLOAT
                    );
                """)
            conn.commit()
            cursor.execute("SELECT * FROM masses_bilan")
            data = cursor.fetchall()
            if not data:
                messagebox.showwarning("Données manquantes", "Aucune donnée disponible dans la base.")
                return
            return data
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des données : {e}")
        finally:
            cursor.close()
            conn.close()

# Afficher toutes les données enregistrées dans la base de données
def display_data():
    data = load_data()
    data_tree.delete(*data_tree.get_children())  # Clear the table first
    if data:
        for d in data:
            data_tree.insert("", "end", values=d[1:])

# Suppression des données d'une année
def delete_year():
    annee = simpledialog.askinteger("Suppression", "Entrez l'année à supprimer :")
    if annee:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM masses_bilan WHERE annee = %s", (annee,))
                conn.commit()
                messagebox.showinfo("Succès", f"Données de l'année {annee} supprimées.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer : {e}")
            finally:
                cursor.close()
                conn.close()
                display_data()

# Affichage du graphique
def plot_ratios():
    try:
        data = load_data()
        print(data)

        annees = [row[1] for row in data]
        actif_immobilise = [row[2] for row in data]
        actif_circulant = [row[3] for row in data]
        total_actif = [row[4] for row in data]
        capitaux_propres = [row[5] for row in data]
        passif_long_terme = [row[6] for row in data]
        passif_circulant = [row[7] for row in data]
        resultat_net = [row[8] for row in data]
        chiffre_d_affaires = [row[9] for row in data]

        rs = [(cp * 100) / ai if ai not in [0, None] else 0 for cp, ai in zip(capitaux_propres, actif_immobilise)]
        rde = [(plt) / cp if cp not in [0, None] else 0 for plt, cp in zip(passif_long_terme, capitaux_propres)]
        rlg = [(ac) / pc if pc not in [0, None] else 0 for ac, pc in zip(actif_circulant, passif_circulant)]
        roe = [(rn * 100) / cp if cp not in [0, None] else 0 for rn, cp in zip(resultat_net, capitaux_propres)]
        roa = [(rn * 100) / ta if ta not in [0, None] else 0 for rn, ta in zip(resultat_net, total_actif)]
        print(rs, rde, rlg, roe, roa)
        style.use('ggplot')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(annees, rs, label="Ratio de solvabilité", marker="o")
        ax.plot(annees, roe, label="Rentabilité des capitaux propres", marker="o")
        ax.plot(annees, roa, label="Rentabilité des actifs", marker="o")
        ax.set_xlabel('Année')
        ax.set_ylabel('Valeur')
        ax.set_title("Évolution des Ratios (en %)")
        ax.legend()
        # fig.show()
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(annees, rde, label="Ratio d'endettement", marker="o")
        ax2.plot(annees, rlg, label="Ratio de liquidité générale", marker="o")
        ax2.set_xlabel('Année')
        ax2.set_ylabel('Valeur')
        ax2.set_title("Évolution des Ratios")
        ax2.legend()
        # fig2.show()
        container_frame = tk.Frame(db_frame)
        container_frame.pack(fill=tk.BOTH, expand=True)
        
        # Affichage du graphique dans l'interface Tkinter
        graph_frame = tk.Frame(container_frame)
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        graph_frame2 = tk.Frame(container_frame)
        graph_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        canvas2 = FigureCanvasTkAgg(fig2, master=graph_frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'affichage du graphique : {e}")
        root.quit()

# Interface pour l'analyse des ratios (première interface)
def show_ratio_analysis():
    ratio_analysis_frame.pack(fill="both", expand=True)
    db_frame.pack_forget()

# Interface pour la gestion de la base de données (seconde interface)
def show_db_management():
    db_frame.pack(fill="both", expand=True)
    ratio_analysis_frame.pack_forget()

# Fonction de sortie
def quit_app():
    root.quit()

# Fonction pour charger et traiter le fichier Excel
def load_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            data = pd.read_excel(file_path)
            data.drop(["Bilan consolidé", "Unnamed: 1"], axis=1, inplace=True)
            data.drop(index=[0, 1, 2], inplace=True)
            data.columns = ["Postes Actif", "Montants Actif", "Postes Passif", "Montants Passif"]

            # Filtrage des masses
            actif_labels_of_interest = ["Actif immobilisé", "Actif circulant", "Total Actif"]
            data_ = {
                "Postes": data["Postes Actif"],
                "Montants": data["Montants Actif"],
            }
            data_actif = pd.DataFrame(data_)
            filtered_actif = data_actif[data_actif["Postes"].isin(actif_labels_of_interest)]

            passif_labels_of_interest = ["Capitaux propres de l'ensemble consolidé", "Passif à long terme", "Passif circulant"]
            data_ = {
                "Postes": data["Postes Passif"],
                "Montants": data["Montants Passif"],
            }
            data_passif = pd.DataFrame(data_)
            filtered_passif = data_passif[data_passif["Postes"].isin(passif_labels_of_interest)]

            # Feuille CPC
            data_2 = pd.read_excel("bilan_resultat.xlsx", sheet_name=1)
            data_2.drop(["CPC Consolidé", "Unnamed: 1", "Unnamed: 2", "Unnamed: 3"], axis = 1, inplace = True)
            data_2.drop(index=[0, 1, 2], inplace = True)
            data_2.columns = ["Postes", "Montants"]
            cr_labels_of_interest = ["Résultat consolidé", "chiffres d'affaires"]
            filtered_data_2 = data_2[data_2["Postes"].isin(cr_labels_of_interest)]
            
            postes = {key: 0 for key in actif_labels_of_interest + passif_labels_of_interest + cr_labels_of_interest}
            for key in actif_labels_of_interest:
                postes[key] = filtered_actif.loc[filtered_actif["Postes"] == key, "Montants"].values[0]
            for key in passif_labels_of_interest:
                postes[key] = filtered_passif.loc[filtered_passif["Postes"] == key, "Montants"].values[0]
                
            for key in cr_labels_of_interest:
                postes[key] = filtered_data_2.loc[filtered_data_2["Postes"] == key, "Montants"].values[0]
                
            # Calcul des ratios
            rs = (postes["Capitaux propres de l'ensemble consolidé"] * 100) / postes["Actif immobilisé"]
            roe = (postes["Résultat consolidé"] * 100) / postes["Capitaux propres de l'ensemble consolidé"]
            roa = (postes["Résultat consolidé"] * 100) / postes["Total Actif"]
            rde = postes["Passif à long terme"] / postes["Capitaux propres de l'ensemble consolidé"]
            rlg = postes["Actif circulant"] / postes["Passif circulant"]

            # Mettre à jour le tableau des résultats
            print(postes)
            display_results(rs, roe, roa, rde, rlg)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du traitement du fichier : {e}")

# Fonction pour afficher les résultats dans le tableau des ratios
def display_results(rs, roe, roa, rde, rlg):
    ratios_tree.delete(*ratios_tree.get_children())  # Clear the table first
    ratios_tree.insert("", "end", values=("Ratio de solvabilité", round(rs, 2), "Indicateur de la capacité de financement"))
    ratios_tree.insert("", "end", values=("Rentabilité des capitaux propres", round(roe, 2), "ROE"))
    ratios_tree.insert("", "end", values=("Rentabilité des actifs", round(roa, 2), "ROA"))
    ratios_tree.insert("", "end", values=("Ratio d'endettement", round(rde, 2), "Indicateur du niveau d'endettement"))
    ratios_tree.insert("", "end", values=("Ratio de liquidité générale", round(rlg, 2), "Indicateur de liquidité à court terme"))

# Fonction pour enregistrer manuellement les données
def manual_entry():
    try:
        postes = {
            "Actif immobilisé": float(actif_entry.get()),
            "Actif circulant": float(circulant_entry.get()),
            "Capitaux propres de l'ensemble consolidé": float(capitaux_entry.get()),
            "Passif à long terme": float(long_term_entry.get()),
            "Passif circulant": float(circulant_passif_entry.get()),
            "Total Actif": float(total_actif_entry.get()),
            "Résultat consolidé": float(resultat_net_entry.get())
        }
        # Calculs des ratios à partir des données saisies manuellement
        rs = (postes["Capitaux propres de l'ensemble consolidé"] * 100) / postes["Actif immobilisé"]
        rde = (postes["Passif à long terme"]) / postes["Capitaux propres de l'ensemble consolidé"]
        rlg = (postes["Actif circulant"]) / postes["Passif circulant"]
        roe = (postes["Résultat consolidé"] * 100) / postes["Capitaux propres de l'ensemble consolidé"]
        roa = (postes["Résultat consolidé"] * 100) / postes["Total Actif"]

        display_results(rs, roe, roa, rde, rlg)
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

if __name__ == "__main__":
    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Analyse Bilan Comptable")
    root.geometry("800x800")

    # Menu de navigation
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Menu "Navigation"
    navigation_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Navigation", menu=navigation_menu)
    navigation_menu.add_command(label="Calcul des Ratios", command=show_ratio_analysis)
    navigation_menu.add_command(label="Gestion de la Base de Données", command=show_db_management)
    navigation_menu.add_command(label="Quitter", command=quit_app)

    ###### Frame pour le calcul des ratios
    ratio_analysis_frame = tk.Frame(root)
    ratio_analysis_frame.pack(fill="both", expand=True)

    # Frame pour la saisie manuelle et l'upload du fichier
    frame_input = tk.Frame(ratio_analysis_frame, bg="#ffffff")
    frame_input.pack(padx=20, pady=20, fill="both", expand=True)

    # Frame pour le tableau des ratios
    frame_table = tk.Frame(ratio_analysis_frame, bg="#ffffff", bd=2, relief="solid")
    frame_table.pack(padx=20, pady=20, fill="both", expand=True)

    # Titre du tableau
    table_title = tk.Label(frame_table, text="Ratios Financiers", font=("Times New Roman", 18, "bold"), bg="#ffffff", fg="#2c3e50")
    table_title.grid(row=0, column=0, columnspan=3, pady=10)

    # Configuration du tableau des ratios (Treeview)
    columns = ("Nom du Ratio", "Valeur", "Interprétation")
    ratios_tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=5)
    ratios_tree.grid(row=1, column=0, columnspan=3, pady=20, sticky="nsew")

    # Définir les en-têtes
    ratios_tree.heading("Nom du Ratio", text="Nom du Ratio")
    ratios_tree.heading("Valeur", text="Valeur")
    ratios_tree.heading("Interprétation", text="Interprétation")

    # Style du tableau
    ratios_tree.column("Nom du Ratio", width=250, anchor="w", stretch=True)
    ratios_tree.column("Valeur", width=100, anchor="center", stretch=True)
    ratios_tree.column("Interprétation", width=300, anchor="w", stretch=True)

    # Configurer le redimensionnement automatique des colonnes
    frame_table.grid_columnconfigure(0, weight=1)
    frame_table.grid_columnconfigure(1, weight=1)
    frame_table.grid_columnconfigure(2, weight=1)

    # Boutons pour charger un fichier et effectuer une saisie manuelle
    load_button = tk.Button(frame_input, text="Charger un fichier Excel", command=load_excel_file, bg="#3498db", fg="white", font=("Times New Roman", 13), relief="groove", bd=4)
    load_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

    manual_button = tk.Button(frame_input, text="Saisie manuelle", command=manual_entry, bg="#DCD51A", fg="white", font=("Times New Roman", 13))
    manual_button.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

    # Champs pour saisie manuelle
    actif_label = tk.Label(frame_input, text="Actif immobilisé:", bg="#ffffff", font=("Times New Roman", 13))
    actif_label.grid(row=1, column=0, pady=5, sticky="e")
    actif_entry = tk.Entry(frame_input, font=("Times New Roman", 13), width=15)
    actif_entry.grid(row=1, column=1, pady=5, sticky="ew")

    circulant_label = tk.Label(frame_input, text="Actif circulant:", bg="#ffffff", font=("Times New Roman", 13))
    circulant_label.grid(row=2, column=0, pady=5, sticky="e")
    circulant_entry = tk.Entry(frame_input, font=("Times New Roman", 13), width=15)
    circulant_entry.grid(row=2, column=1, pady=5, sticky="ew")

    total_actif_label = tk.Label(frame_input, text="Total Actif:", bg="#ffffff", font=("Times New Roman", 13))
    total_actif_label.grid(row=3, column=0, pady=5, sticky="e")
    total_actif_entry = tk.Entry(frame_input, font=("Times New Roman", 13), width=15)
    total_actif_entry.grid(row=3, column=1, pady=5, sticky="ew")

    capitaux_label = tk.Label(frame_input, text="Capitaux propres de l'ensemble consolidé:", bg="#ffffff", font=("Times New Roman", 13))
    capitaux_label.grid(row=4, column=0, pady=5, sticky="e")
    capitaux_entry = tk.Entry(frame_input, font=("Times New Roman", 13), width=15)
    capitaux_entry.grid(row=4, column=1, pady=5, sticky="ew")

    long_term_label = tk.Label(frame_input, text="Passif à long terme:", bg="#ffffff", font=("Times New Roman", 13))
    long_term_label.grid(row=5, column=0, pady=5, sticky="e")
    long_term_entry = tk.Entry(frame_input, font=("Times New Roman", 13), width=15)
    long_term_entry.grid(row=5, column=1, pady=5, sticky="ew")

    circulant_passif_label = tk.Label(frame_input, text="Passif circulant:", bg="#ffffff", font=("Times New Roman", 13))
    circulant_passif_label.grid(row=6, column=0, pady=5, sticky="e")
    circulant_passif_entry = tk.Entry(frame_input, font=("Times New Roman", 13), width=15)
    circulant_passif_entry.grid(row=6, column=1, pady=5, sticky="ew")

    resultat_net_label = tk.Label(frame_input, text="Résultat net:", bg="#ffffff", font=("Times New Roman", 13))
    resultat_net_label.grid(row=7, column=0, pady=5, sticky="e")
    resultat_net_entry = tk.Entry(frame_input, font=("Times New Roman", 13), width=15)
    resultat_net_entry.grid(row=7, column=1, pady=5, sticky="ew")

    ###### Frame pour la gestion de la base de données
    db_frame = tk.Frame(root)
    db_frame.pack_forget()

    # Saisie manuelle des données à enregistrer
    # Frame pour l'affichage des données enregistrées
    frame_table_2 = tk.Frame(db_frame, bg="#ffffff")
    frame_table_2.pack(padx=20, pady=20, fill="both", expand=True)
    
    # Configuration du tableau des données annuelles (Treeview)
    columns_2 = ("Année", "Actif immobilisé", "Actif circulant", "Total actif", "Capitaux propres", "Passif à long terme", "Passif circulant", "Résultat net", "Chiffre d'affaires")
    data_tree = ttk.Treeview(frame_table_2, columns=columns_2, show="headings", height=5)
    data_tree.grid(row=1, column=0, columnspan=3, pady=20, sticky="nsew")

    # Définir les en-têtes et le style du tableau
    for i, name in enumerate(columns_2):    
        data_tree.heading(name, text=name)
        data_tree.column(name, width=100, anchor="w", stretch=True)

        # Configurer le redimensionnement automatique des colonnes
        frame_table_2.grid_columnconfigure(i, weight=1)
    
    # Afficher les données de la base de données
    display_data()
    
    # Bouton d'ajout de nouvelles données
    add_button = tk.Button(db_frame, text="Ajouter des données", bg="#D9C057", command=add_data)
    add_button.pack()
    
    # Suppression d'une année
    delete_button = tk.Button(db_frame, text="Supprimer une année", bg="#db3e69", command=delete_year)
    delete_button.pack(pady=5)

    # Affichage des graphes
    plot_button = tk.Button(db_frame, text="Afficher l'évolution des ratios", command=plot_ratios, bg="#1F23DB", fg="white", font=("Times New Roman", 13))
    plot_button.pack(pady=5)
    
    # Bouton de sortie de l'application
    quit_button = tk.Button(root, text="Fermer l'application", command=quit_app, bg="#DB1F00", fg="white", font=("Times New Roman", 13))
    quit_button.pack(pady=10)

    
    # Lancer l'application avec l'interface de calcul des ratios par défaut
    show_ratio_analysis()
    display_results(0, 0, 0, 0, 0)
    

    # Lancement de l'interface graphique
    root.mainloop()
