# **Grocery Manager Application** 🛒  
*A Feature-Packed Grocery List Manager with Recipe Suggestions, PDF Integration, and Notifications*

---

## 📋 **Table of Contents**
1. [Introduction](#introduction)  
2. [Key Features](#key-features)  
3. [Technologies Used](#technologies-used)  
4. [Setup Guide](#setup-guide)  
5. [Usage Instructions](#usage-instructions)  
6. [Key Functionalities](#key-functionalities)  
7. [API Integration](#api-integration)  
8. [Learnings and Challenges](#learnings-and-challenges)  
9. [Future Scope](#future-scope)  
10. [Acknowledgments](#acknowledgments)  

---

## 🚀 **Introduction**  
The **Grocery Manager Application** is a powerful tool to organize your shopping list, suggest recipes based on your ingredients, and provide useful features like PDF export, PDF import, and item expiry notifications. Built using **PyQt5**, the application delivers an interactive and visually appealing user interface, making grocery planning simple and enjoyable.

---

## 🔑 **Key Features**  
1. **Dynamic Shopping List Management**:  
   - Add, remove, and manage grocery items easily.  

2. **Recipe Suggestions**:  
   - Automatically suggests recipes based on your shopping list.  
   - Integration with the **Spoonacular API** for real-time recipe fetching.  
   - Allows direct YouTube search for recipes related to the ingredients.  

3. **PDF Integration**:  
   - **Download List as PDF**: Export your shopping list to a neat PDF format.  
   - **Upload List from PDF**: Load an existing grocery list from a PDF file.  

4. **Notifications**:  
   - Displays **expiry notifications** for critical items in your list.  
   - Sends tray notifications for items nearing expiry (1-2 days left).  

5. **Modern and Clean UI**:  
   - Built with **PyQt5** with a modern and professional design.  
   - Includes animations and a stylish dark theme for enhanced user experience.

---

## 🛠️ **Technologies Used**  
- **Python 3.x**: Core programming language.  
- **PyQt5**: For building the GUI application.  
- **Spoonacular API**: For fetching recipe suggestions.  
- **FPDF**: For creating and exporting PDFs.  
- **PyPDF2**: For reading and extracting data from PDF files.  
- **Requests**: For API integration.  
- **Webbrowser**: To open recipe videos directly on YouTube.  

---

## 📦 **Setup Guide**

1. **Clone the Repository**  
   Clone the project to your local machine:  
   ```bash
   git clone https://github.com/yourusername/grocery-manager.git
   cd grocery-manager
   ```

2. **Install Dependencies**  
   Install the required libraries using `pip`:  
   ```bash
   pip install PyQt5 fpdf PyPDF2 requests
   ```

3. **Run the Application**  
   Execute the Python file to launch the app:  
   ```bash
   python grocery_manager.py
   ```

---

## 🧑‍💻 **Usage Instructions**

### **Main Functionalities**  
1. **Add Items to Shopping List**:  
   - Enter grocery items in the text area and click **"Add to List"**.  

2. **Remove Items**:  
   - Select an item from the list and click **"Remove Selected"**.

3. **Recipe Suggestions**:  
   - Click **"Suggest Recipes"** to fetch recipe ideas using the Spoonacular API.  
   - Click a recipe to search for its tutorial on **YouTube**.

4. **PDF Integration**:  
   - **Download PDF**: Save the current shopping list as a PDF.  
   - **Upload PDF**: Load a grocery list from an existing PDF file.

5. **Notifications**:  
   - Check the "Notifications" section to see expiring items.  
   - Receive system tray notifications for items nearing expiry.

---

## 🔗 **API Integration**
The app uses the **Spoonacular API** to fetch recipe suggestions:  
- API Endpoint: `https://api.spoonacular.com/recipes/findByIngredients`  
- Parameters:  
   - `ingredients`: List of grocery items entered by the user.  
   - `number`: Number of recipe suggestions (default: 5).  
   - `apiKey`: Your Spoonacular API key.  

**API Key Setup**: Replace the placeholder API key in the code:  
```python
api_key = "YOUR_SPOONACULAR_API_KEY"
```

---

## 💡 **Learnings and Challenges**
### **Key Learnings**:
- Working with **PyQt5** for GUI development and animations.  
- Integrating external APIs (Spoonacular API) for fetching live data.  
- Using **FPDF** and **PyPDF2** for PDF export and import functionalities.  
- Implementing system tray notifications and background timers.  

### **Challenges Faced**:  
- Optimizing API responses for recipe suggestions.  
- Handling PDF parsing and ensuring text extraction accuracy.  
- Designing a clean and modern UI that remains responsive and user-friendly.

---

## 🌟 **Future Scope**
- Add real-time **data visualization** for shopping trends.  
- Integrate more APIs for recipe videos and nutritional information.  
- Implement **cloud storage** to save and sync shopping lists across devices.  
- Enhance expiry date tracking with a calendar integration.

---

## 🙌 **Acknowledgments**  
Special thanks to:  
- **PyQt5** for simplifying GUI design.  
- **Spoonacular API** for providing recipe suggestions.  
- Open-source tools like **FPDF** and **PyPDF2** for PDF functionalities.  

---

## 📬 **Connect With Me**  
- **LinkedIn**: [Your LinkedIn Profile](https://github.com/Lakshya300104)  
- **GitHub**: [Your GitHub Profile](https://www.linkedin.com/in/lakshya-arora-76a567259/)  
- **Email**: lakshya13004@gmail.com 

---

### **#Python #PyQt5 #GroceryManager #APIs #FPDF #PDFIntegration #RecipeSuggestions #CodingProject**
