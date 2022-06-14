import pandas as pd
import matplotlib.pyplot as plt

# Εισαγωγή Στοιχείων
# Πίνακας των Χρηστών
U=pd.read_csv("users.csv","\t")
# Πίνακας των Ταινιών
M=pd.read_csv("movies.csv","\t", encoding="ISO-8859-1")
# Πίνακας των Βαθμολογιών
R=pd.read_csv("ratings.csv",";", encoding="ISO-8859-1")

# Συνάρτηση που βρίσκει την ομοιότητα μεταξύ δυο χρηστών
def common(id1,id2):
    d=0
    # Παίρνουμε την λϊστα των χρηστών
    LU=list(U["user_id"])
    try:
        # Ελέγχουμε αν υπάρχουν οι δύο χρήστες
        idx1=LU.index(id1)
        idx2=LU.index(id2)
        # Κοινά χαρακτηριστικά όπως ηλικία φύλο...
        if(U["age_desc"][idx1]==U["age_desc"][idx2]):
            d=d+2
        if(U["gender"][idx1]==U["gender"][idx2]):
            d=d+1
        if(U["occ_desc"][idx1]==U["occ_desc"][idx2]):
            d=d+1
        if(U["occupation"][idx1]==U["occupation"][idx2]):
            d=d+1
           
       
        # Αν έχουν αρκετά κοινά μετράμε πόσες κοινές ταινίες έχουν
        if(d>3):
            # Παίρνουμε τις ταινίες του πρώτου χρήστη
            R1=R[R["user_id"]==id1]
            # Παίρνουμε τις ταινίες του δεύτερου χρήστη
            R2=R[R["user_id"]==id2]
            
            # Βρίσκουμε τις κοινές ταινίες
            R3=R1[R1["movie_id"].isin(list(R2["movie_id"]))]
            # Πόσο κοινές είναι οι βαθμολογίες, ίδιο γούστο
            for m in list(R3["movie_id"]):
                rr1=R1[R1["movie_id"]==m]
                rr2=R2[R2["movie_id"]==m]
                if(abs(rr1["rating"].iloc[0]-rr2["rating"].iloc[0])<2):
                    d=d+0.5
    except:
        d=0
    # Επιστρέφουμε το βάρος, ομοιότητα
    return d

# Main Program
while(True):
    # Μενού
    print("1. Recommend a movie for a user")
    print("2. Show Plots of Data")
    print("3. Exit")
    print("----------------------------------------")
    choice=input("Give choice: ")
    
    if(choice=="1"):    
            try:
                # Βασικός χρήστης που προτείνουμε ταινίες
                idu=int(input("Give user id: "))
                
                # Λίστα όλων των χρηστών
                UL=list(U["user_id"])
                
                # Πού βρίσκεται ο χρήστης στη λίστα
                inx=UL.index(idu)
                
                # Χρήστες με κοινά ενδιαφέροντα
                L={}
                for i in UL:
                    if(i!=idu):
                        L[i]=common(idu,i)
                
                
                L2=sorted(L.items(), key=lambda x: x[1], reverse=True) #Φθίνουσα
                x=L2[0][0] # id του χρήστης με τα περισσότερα κοινά
                R1=R[R["user_id"]==idu] 
                R2=R[R["user_id"]==x]
                try:
                    # Ταινλιες που δεν έχει δεί ο βασικός χρήστης
                    R3=R2[~R2["movie_id"].isin(list(R1["movie_id"]))]
                    R4=R3[R3["rating"]==5]
                    for m in list(R4["movie_id"]):
                        mm=M[M["movie_id"]==m]
                        print(mm["title"].iloc[0])
                    print("\n")
                except:
                   print("error")
                
            except:
                print("user couldnt found")
    
    if(choice=="2"):
        plt.hist(U["gender"])
        plt.show()
        
        plt.hist(U["age"])
        plt.show()
        
        C={}
        Mv=[]
        for m in range(len(M)):
           
            mm=M["genres"][m]
            kat=mm.split("|")
            x=[]
            x.append(M["movie_id"][m])
            x.append(kat)
            Mv.append(x)
            for cc in kat:
                try:
                    C[cc]=C[cc]+1
                except:
                    C[cc]=1
        
        plt.bar(range(len(C)), list(C.values()), align='center')
        plt.xticks(range(len(C)), list(C.keys()))
        plt.show()
    
    if(choice=="3"):
        break
