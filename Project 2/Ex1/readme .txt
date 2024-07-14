
Το σχήμα της βάσης δεδομένων αποτελείται από τους παρακάτω πίνακες:

Director: Πληροφορίες σχετικά με τους σκηνοθέτες.
Nationality: Πληροφορίες σχετικά με την εθνικότητα των σκηνοθετών.
Movie: Πληροφορίες σχετικά με τις ταινίες.
Country: Πληροφορίες σχετικά με τις χώρες.
City: Πληροφορίες σχετικά με τις πόλεις.
Sponsor: Πληροφορίες σχετικά με τους χορηγούς.
Actor: Πληροφορίες σχετικά με τους ηθοποιούς.
Role: Πληροφορίες σχετικά με τους ρόλους που αναλαμβάνουν οι ηθοποιοί.
Actor Characteristic Quality: Πληροφορίες σχετικά με τα χαρακτηριστικά ποιότητας των ηθοποιών.
Physical Characteristics: Πληροφορίες σχετικά με τα φυσικά χαρακτηριστικά των ηθοποιών.
Mental Characteristic: Πληροφορίες σχετικά με τα ψυχολογικά χαρακτηριστικά των ηθοποιών.
Training Program: Πληροφορίες σχετικά με τα προγράμματα εκπαίδευσης των ηθοποιών.
Technical Characteristic: Πληροφορίες σχετικά με τα τεχνικά χαρακτηριστικά των ηθοποιών.
Genre: Πληροφορίες σχετικά με τα είδη των ταινιών.
Contract: Πληροφορίες σχετικά με τα συμβόλαια των ηθοποιών.
Competition: Πληροφορίες σχετικά με τους διαγωνισμούς.
Award: Πληροφορίες σχετικά με τα βραβεία.
Script: Πληροφορίες σχετικά με τα σενάρια των ταινιών.
ScriptSegment: Πληροφορίες σχετικά με τα τμήματα των σεναρίων.
Social Media Page: Πληροφορίες σχετικά με τις σελίδες στα social media.
Friendship: Πληροφορίες σχετικά με τη φιλία μεταξύ χρηστών.
Player: Πληροφορίες σχετικά με τους παίκτες που συμμετέχουν σε διαγωνισμούς.

οι συσχετίσεις μεταξύ των πινάκων είναι οι εξής:
(non identifying για τα χαρακτηριστικά που μπορούν να υπάρχουν ανεξάρτητα ή αν μπορεί να υπάρχουν περιπτώσεις όπου δεν υπάρχει σύνδεση με κάποιο πίνακα)

1:n Player - Game : non identifying γιατι ο player είναι η οντότητα που υπάρχει ανεξάρτητα από τα παιχνίδια 
Τα παιχνίδια είναι σχετικά με τον παίκτη αλλά δεν τον αναγνωρίζουν αποκλειστικά. Ετσι τα δεδομένα του παίκτη δεν είναι απαραίτητο να είναι μοναδικά για κάθε παιχνίδι. 
Κάθε εγγραφή στο game συσχετίζεται με έναν Player, αλλά δεν απαιτείται να τον αναγνωρίζει πλήρως.

1:n Player Characteristic : identifying γιατι τα χαρακτηριστικά ειναι στένα συνδεδεμένα με τον player

1:n Game - Director : identifying ένα game μπορει να έχει έναν ή πολλούς directors

1:n Director - Nationality :identifying ένας director με ένα ή πολλά nationality.

1:n Director - Look Up to : non identifying ένας με πολλά πράγρατα που μπορεί να έχει σάν πρότυπα. 

1:n Director - Movies : identifying ένας σκηνοθέτης σκηνοθετεί πολλές ταινίες

1:n Movie - Genre : identifying μια ταινία έχει πολλά Είδη 

1:1 Movie - domestic Schenery και 1:n με το international Scenery 
Μία ταινία ένα εγχώριο σκηνικό, μια ταινία ένα ή πολλά παγκόσμια σκηνικά

n:m international - country: ένα ή πολλά σκηνικά με μία ή πολλες χώρες

1:1 domestic - city : non identifying ένα domestic μία πολη

n:m sponsor - movie : πολλοι σπόνσορες έχουν πολλές ταινίες

1:1 movie - script και 1:n script - Script - Segment: identifying εδώ εχουμε μία ταινία ένα σενάριο και αντιστοιχα ένα σενάριο πολλάπλα Segments

1:n script Segment non identifying στο ίδιο για να εξασφαλιστουν τα previous segments έαν σβηστεί ένα segment να μην σβηστούν και τα προηγούμενα. 

1:n movie - actor :identifying Μια ταινία μπορει να έχει πολλους ηθοποιούς

1:1 actor - country : non identifying ένας ηθοποιος απο ποια χώρα είναι

1:n actor - role : non identifying ένας ηθοποιους μπορει να έχει πολλους ρόλους, εδώ τα χαρακτηριστικά μπορει να ειναι null για αυτο δεν ειναι τσεκαρισμένο το not null
δηλαδή μπόρει να ειναι πρωταγωνιστής και να ειναι συμπληρομενο το χαρακτηριστικο αυτο και να μην είναι και 2ος ρόλος άρα μπορεί το χαρακτηριστικό αυτο να έχει τιμή μηδέν.

1:n actor με τα Psysical Mental και technical χαρακτηριστικά του. 

1:n τα χαρακτηριστικά με το Actor Characteristic Quality identifying όπου κάθε ένα έχει και ένα rating

1:1 actor - Training Program : non identifying ένας ηθοποιός μπορεί να παρακολούθησει ένα training program

1:1 Training Program - Technical Characteristis non identifying ώστε να γίνεται η συνδεση πως το training program μπορεί να επιρρεάσει τα χαρακτηριστικά αυτα του ηθοποιού.

1:n Movie - Competition: non identifying Μία ταινία μπορει να συμμετέχει σε πολλές διοργανώσεις

1:n Director - Competition: non identifying ένας σκηνοθέτης μπορεί να συμμετέχει σε πολλές διοργανώσεις. 

1:1 Competition - Country : non identifying Μία διοργάνωση μπορει να έχει μία χώρα στην οποία γίνεται.

1:1 Competition - Competition Stats: identifying Η διοργάνωση με τα στατιστικά

1:n Movie - Competition stats: non identifying Το σύνολο των στατιστίκων της ταινίας για τη διοργάνωση.

1:n Competition - Social Media Page: non identifying Κάθε διοργάνωση έχει πολλές σελίδες στα κοινωνικά δίκτυα. 

1:n Director Social Media Page: non identifying: Ένας σκηνοθέτης έχει ένα η πολλά κοινωνικά δίκτυα. 

1:1 Social Media - Friendship: non identifying για τις φιλίες στα κοινωνικά δίκτυα. 

1:n director - Director Like: non identifying likes των σκηνωθετών για την ταινία.























