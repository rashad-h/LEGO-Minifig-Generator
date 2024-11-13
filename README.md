# LEGO Minifigure Generation Project 🎨🤖

This project uses AI-powered natural language processing to generate custom LEGO minifigure part recommendations based on user-provided descriptions. By leveraging transformer models and fine-tuning techniques, the model understands text descriptions of minifigures and outputs recommended LEGO parts with specific details, such as color and print.

## 🚀 Project Overview

Inspired by the vast array of LEGO minifigures and parts, this project combines NLP and machine learning to provide users with minifigure customization options based on text input. Users can enter a description like "Batman in a black suit with a cape and white goggles," and the model will generate a list of compatible LEGO parts based on available data.

### Example Output

- **Input**: `"Spiderman in white suit"`
- **Output**:
  - **Headwear**: "Helmet with Spiderman Logo Print <Black>"
  - **Lower Body**: "Hips and White Legs with Silver Webbing Print <White>"
  - **Upper Body**: "Torso Armor with Silver Webbing Print, Red Arms and Hands <White>"

## 📂 Project Structure

- **Database/** - Contains training and validation code for creating the database with descriptions of LEGO minifigures and parts.
- **training/** - Main code directory containing model training, tokenization, and inference scripts.
- **lora_model/** - Directory for saved models and checkpoints.

## 🛠️ Key Features

1. **Text-to-Part Generation**: Generates detailed LEGO minifigure parts based on natural language descriptions.
2. **Transformer-based Model**: Fine-tunes LLaMA model with Unsloth for high-quality, contextually relevant output.
3. **Customizable Inputs**: Accepts detailed or brief descriptions, adapting recommendations accordingly.
4. **Cosine Similarity for Post-Processing**: Maps generated descriptions to actual LEGO part IDs using similarity matching, ensuring accurate part retrieval. (in progress)

## ⚙️ Technical Approach

The project uses a transformer-based model, **LLaMA**, fine-tuned with **Unsloth** for sequence generation, and cosine similarity for accurate part matching. Below is a technical breakdown:

1. **Data Retrival**: Created a bot to datamine the LEGO minifigures part descriptions of the web.
2. **Data Preprocessing**: Cleaned and tokenized minifigure and part descriptions to improve training quality.
3. **Model Architecture**: LLaMA, a transformer model, trained to map minifigure descriptions to a sequence of part descriptions.
4. **Fine-Tuning**: Unsloth was used to simplify the fine-tuning process on domain-specific data.
5. **Post-Processing**: Uses cosine similarity to match generated descriptions to actual part IDs for precise recommendations. (in progress)

