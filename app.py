from flask import Flask, jsonify, request
from flask_cors import CORS 
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('LibraryDB.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Paper and Pixel API is running successfully!"})

##  FOR ALL BOOKS AND FILTERS ON HOME PAGE (JUST THEIR CARDS' DETAILS)

@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        category_id = request.args.get('category_id')

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                b.[book_id],        -- row[0]
                b.[book_name],      -- row[1]
                b.[page_num],       -- row[2]
                w.[writer_name],    -- row[3]
                c.[category_name],  -- row[4]
                b.[image_name],      -- row[5]
                b.[summary]         -- row[6]
            FROM [books] b
            LEFT JOIN [writers] w ON b.[writer_id] = w.[writer_id]
            LEFT JOIN [categories] c ON b.[category_id] = c.[category_id]
        """

        if category_id:
            query += " WHERE b.category_id = ?"
            cursor.execute(query, (category_id,))
        else:
            cursor.execute(query)

        rows = cursor.fetchall()
        conn.close()

        book_list = []

        for row in rows:
            image_file = row[5] if (len(row) > 5 and row[5]) else "default-cover.jpg"
            book_list.append({
                "id": row[0],
                "title": row[1],
                "page_num": row[2],
                "author": row[3] if row[3] else "Unknown",
                "category": row[4] if row[4] else "General",
                "image_url": f"pictures/{image_file}",
            })

        return jsonify(book_list)

    except Exception as e:
        print("ERROR DETAIL: ", str(e))
        return jsonify({"error: ", str(e)}), 500

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_single_book(book_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                SELECT
                    b.[book_id],        -- row[0]
                    b.[book_name],      -- row[1]
                    b.[page_num],       -- row[2]
                    w.[writer_name],    -- row[3]
                    c.[category_name],  -- row[4]
                    b.[image_name],     -- row[5]
                    b.[summary]         -- row[6]
                FROM [books] b
                LEFT JOIN [writers] w ON b.[writer_id] = w.[writer_id]
                LEFT JOIN [categories] c ON b.[category_id] = c.[category_id]
                WHERE b.[book_id] = ?   
            """

            cursor.execute(query, (book_id,))
            row = cursor.fetchone()
            conn.close()


            if row:
                image_file = row[5] if (len(row) > 5 and row[5]) else "default-cover.jpg"
                summary_text = row[6] if (len(row) > 6 and row[6]) else "No summary available"

                book_data = {
                    "id": row[0],
                    "title": row[1],
                    "page_num": row[2],
                    "author": row[3] if row[3] else "Unknown",
                    "category": row[4] if row[4] else "General",
                    "image_url": f"pictures/{image_file}",
                    "summary": summary_text
                }
                return jsonify(book_data)
            else:
                return jsonify({"error": "Couldn't find the book!"}), 404

        except Exception as e:
            print("ERROR DETAIL:", str(e))
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)