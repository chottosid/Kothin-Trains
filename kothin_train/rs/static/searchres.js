const stations=["Adv. Motiur Rahman","Abdulpur","Aditmari","Ahsanganj","Akhaura","Akkelpur","Alamdanga","Amirabad ","Amnura","Arani","Ashuganj","Atharabari","Azampur","Azim Nagar","B Sirajul Islam","Badarganj","Badherhat","Badiakhali","Baharpur","Bajitpur","Bajra","Bamondanga","Banani","Baramchal","Barhatta","Barkhata","BBSetu_E","BBSetu_W","Benapole","Bhairab_Bazar","Bhanga","Bhanugach","Bhatiary","Bheramara","Bhomradah","Bhuapur","Bidyaganj","Biman_Bandar","Birampur","Boalmari_Bazar","Bogura","Bolakhal","Bonar_Para","Boral_Bridge","Borashi","Brahmanbaria","Burimari","Chandpur","Chandpur_Court","Chandradighalia","Chapai Nawabganj","Chapta","Chatmohar","Chattogram","Chilahati","Chirirbandar","Chitoshi_Road","Choto Bahirbag","Choumuhani","Chuadanga","Cumilla","Darshana_Halt","Dashuria","Daulatpur","Dewanganj_Bazar","Dhaka","Dhaka_Cantonment","Dhalarchar","Dinajpur","Domar","Dublia","Faridpur","Feni","Fulbari","Gachihata","Gafargaon","Gaibandha","Gobra","Gopalganj","Gouripur_Myn","Gunabati","Hajiganj","Haldibari","Harashpur","Hasanpur","Hatibandha","Hemnagar","Hi-Tech City","Hili","Ishwardi","Ishwardi Bypass","Islampur_Bazar","Jamalganj","Jamalpur_Town","Jamtail","Jashore","Jhikargacha","Joydebpur","Joypurhat","Kakonhat","Kalukhali","Kankina","Kashiani","Kashinathpur","Kaunia","Khoksha","Kholahati","Khulna","Kishorganj","Kismat","Kolkata","Kotchandpur","Kulaura","Kuliarchar","Kumarkhali","Kumira","Kurigram","Kushtia Court","Laksam","Lalmonirhat","Lokmanpur","Lolitnagar","Madhnagar","Madhukhali","Mahimaganj","Maijdi Court","Maijgaon","Majhgram","Manikkhali","Meher","Melandah_Bazar","Methikanda","Mirpur","Mirzapur","Modhu_Road","Mohanganj","Montola","Mubarakganj","Mukundapur","Muladhuli","Mymensingh","Nachole","Nandina","Nangolkot","Narayanganj","Narsingdi","Narundi","Natherpetua","Natore","Nayapara","Netrakona","New Jalpaiguri","Nilphamari","Noakhali","Noapara","Pabna","Pachuria","Pahartali","Pakshi","Panchbibi","Pangsha","Parbatipur","Patgram","Pirgacha","Pirganj","Piyarpur","Poradaha","Pukuria","Quasba","Raghabpur","Rajbari","Rajshahi","Rajshahi_Court","Rangpur","Rohanpur","Ruhia","Safdarpur","Saidpur","Santahar","Sararchar","Sardah_Road","Sarishabari","Sathia_Rajapur","Setabganj","SH M Monsur Ali","Shahaji_Bazar","Shahrasti","Shahtali","Shaistaganj","Shamshernagar","Shashidal","Shibganj","Shyamgonj","Sirajganjraipur","Sirajganj_Bazar","Sonaimuri","Sonatola","Sreemangal","Sreepur","Sylhet","Talma","Talora","Tangail","Tantibandha","Tarakandi","Tebunia","Teesta Junction","Thakrokona","Thakurgaon_Road","Tongi","Tushbandar","Ullapara"];
const fromBox = document.getElementById("from");
const suggestionList = document.getElementById("suggestion-list-from");

fromBox.addEventListener("input", () => {
    const query = fromBox.value.toLowerCase();  // Corrected fromBox.value

    // Clear previous suggestions
    suggestionList.innerHTML = "";

    if (query.length >= 2) {
        const filteredSuggestions = stations.filter(suggestion => suggestion.toLowerCase().startsWith(query));
        const maxSuggestions = 5;

        filteredSuggestions.slice(0, maxSuggestions).forEach(suggestion => {
            const li = document.createElement("li");
            li.textContent = suggestion;
            suggestionList.appendChild(li);

            // Add click event listener to suggestion items
            li.addEventListener("click", () => {
                if(toBox.value==suggestion){
                    toBox.value=""; 
                }
                fromBox.value = suggestion;  // Set the input field's value
                suggestionList.innerHTML = "";  // Clear the suggestion list
            });
        });
    }
});

const toBox = document.getElementById("to");
const suggestionList2 = document.getElementById("suggestion-list-to");

toBox.addEventListener("input", () => {
    const query = toBox.value.toLowerCase();  // Corrected toBox.value

    // Clear previous suggestions
    suggestionList2.innerHTML = "";

    if (query.length >= 2) {
        const filteredSuggestions2 = stations.filter(suggestion => suggestion.toLowerCase().startsWith(query));
        const maxSuggestions = 5;

        filteredSuggestions2.slice(0, maxSuggestions).forEach(suggestion => {
            const li = document.createElement("li");
            li.textContent = suggestion;
            suggestionList2.appendChild(li);

            // Add click event listener to suggestion items
            li.addEventListener("click", () => {
                if(fromBox.value==suggestion){
                    fromBox.value="";
                    suggestionList.innerHTML="";
                }
                else{
                    toBox.value = suggestion;  // Set the input field's value
                    suggestionList2.innerHTML = ""; 
                } // Clear the suggestion list
            });
        });
    }
});
