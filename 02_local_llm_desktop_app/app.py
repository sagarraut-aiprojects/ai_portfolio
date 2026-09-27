import customtkinter as ctk
from datetime import datetime
import threading
from tkinter import messagebox

from ollama_client import chat_with_model

from conversation import (
    create_conversation,
    save_conversation,
    load_all_conversations,
    load_conversation,
    delete_conversation
)


# ============================================================
# APPEARANCE
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================
# CONVERSATION MEMORY
# ============================================================

current_conversation = create_conversation()

messages = current_conversation["messages"]


# ============================================================
# CHAT BUBBLE
# ============================================================

class ChatBubble(ctk.CTkFrame):

    def __init__(
        self,
        master,
        text="",
        sender="bot",
        **kwargs
    ):

        super().__init__(
            master,
            fg_color="transparent",
            **kwargs
        )

        is_user = sender == "user"

        if is_user:
            bubble_color = "#2563eb"
            anchor_side = "e"
            justify = "right"
        else:
            bubble_color = "#3a3a3a"
            anchor_side = "w"
            justify = "left"

        # ----------------------------------------------------
        # Message bubble
        # ----------------------------------------------------

        self.bubble = ctk.CTkLabel(
            self,
            text=text,
            wraplength=600,
            justify=justify,
            anchor="w",
            fg_color=bubble_color,
            text_color="white",
            corner_radius=14,
            padx=14,
            pady=10,
            font=("Segoe UI", 12),
        )

        self.bubble.pack(
            anchor=anchor_side,
            padx=10,
            pady=(5, 2)
        )

        # ----------------------------------------------------
        # Timestamp
        # ----------------------------------------------------

        timestamp = ctk.CTkLabel(
            self,
            text=datetime.now().strftime("%H:%M"),
            font=("Segoe UI", 9),
            text_color="#777777",
        )

        timestamp.pack(
            anchor=anchor_side,
            padx=14,
            pady=(0, 5)
        )

    # --------------------------------------------------------
    # Update text while streaming
    # --------------------------------------------------------

    def update_text(self, text):

        self.bubble.configure(
            text=text
        )


# ============================================================
# MAIN APPLICATION
# ============================================================

class ChatbotApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # ====================================================
        # WINDOW
        # ====================================================

        self.title("Prof. Sagar's Local AI")

        self.geometry(
            "900x650"
        )

        self.minsize(
            650,
            500
        )

        # ====================================================
        # GRID
        # ====================================================

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=0
        )

        self.grid_columnconfigure(
             0,
             weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        # ====================================================
        # STATE
        # ====================================================

        self.generating = False

        self.current_ai_bubble = None


        # ====================================================
        # SIDEBAR
        # ====================================================

        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
            fg_color="#151515"
        )

        self.sidebar.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="nsew",
            padx=(0, 8),
            pady=0
        )

        self.sidebar.grid_propagate(False)

        self.new_chat_btn = ctk.CTkButton(
            self.sidebar,
            text="+  New Chat",
            height=42,
            corner_radius=10,
            font=("Segoe UI", 12, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.new_chat
        )

        self.new_chat_btn.pack(
            fill="x",
            padx=12,
            pady=(15, 20)
        )


        self.history_label = ctk.CTkLabel(
            self.sidebar,
            text="CHATS",
            font=("Segoe UI", 10, "bold"),
            text_color="#777777",
            anchor="w"
        )

        self.history_label.pack(
            fill="x",
            padx=16,
            pady=(4, 10)
        )


        self.history_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color="transparent",
            corner_radius=0
        )

        self.history_frame.pack(
            fill="both",
            expand=True,
            padx=6,
            pady=(0, 10)
        )

        # ====================================================
        # CHAT HISTORY
        # ====================================================

        self.chat_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#181818",
            corner_radius=0
        )

        self.chat_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=8,
            pady=(8, 0)
        )

        self.chat_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # ====================================================
        # INPUT SECTION
        # ====================================================

        input_row = ctk.CTkFrame(
            self,
            fg_color="#181818",
            corner_radius=14
        )

        input_row.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=12,
            pady=(6,12)
        )

        input_row.grid_columnconfigure(
            0,
            weight=1
        )

        # ----------------------------------------------------
        # INPUT BOX
        # ----------------------------------------------------

        self.entry = ctk.CTkEntry(
            input_row,
            placeholder_text="Type a message...",
            height=44,
            font=("Segoe UI", 12),
            corner_radius=12
        )

        self.entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 8)
        )

        self.entry.bind(
            "<Return>",
            self.send_message
        )

        # ----------------------------------------------------
        # SEND BUTTON
        # ----------------------------------------------------

        self.send_btn = ctk.CTkButton(
            input_row,
            text="Send",
            width=85,
            height=44,
            corner_radius=12,
            command=self.send_message
        )

        self.send_btn.grid(
            row=0,
            column=1
        )

        # ====================================================
        # WELCOME MESSAGE
        # ====================================================

        self.add_message(
            "Hi! I'm Sagar ai running locally on your computer.\n"
            "How can I help you today?",
            sender="bot"
        )
        self.refresh_sidebar()
        # ====================================================
        # FOCUS INPUT
        # ====================================================

        self.after(
            100,
            self.entry.focus_set
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )


    def new_chat(self):

        global current_conversation, messages

        # Create a new empty conversation
        current_conversation = create_conversation()
        messages = current_conversation["messages"]

        # Clear the current chat window
        for widget in self.chat_frame.winfo_children():
            widget.destroy()

        # Show welcome message
        self.add_message(
            "Hi! I'm Sagar ai running locally on your computer.\n"
            "How can I help you today?",
            sender="bot"
        )

        # Put cursor back in input box
        self.entry.focus_set()    
        self.refresh_sidebar()


    def load_chat(self, conversation_id):

        global current_conversation, messages

        # Load the selected conversation
        conversation = load_conversation(conversation_id)

        if conversation is None:
            return

        # Make it the current conversation
        current_conversation = conversation
        messages = current_conversation["messages"]

        # Clear the current chat window
        for widget in self.chat_frame.winfo_children():
            widget.destroy()

        # Display all saved messages
        for message in messages:

            if message["role"] == "user":
                self.add_message(
                    message["content"],
                    sender="user"
                )

            elif message["role"] == "assistant":
                self.add_message(
                    message["content"],
                    sender="bot"
                )

        # Put cursor back in input box
        self.entry.focus_set()

    def delete_chat(self, conversation_id):

        global current_conversation, messages

        # Delete the JSON file
        delete_conversation(conversation_id)

        # If the deleted conversation is currently open,
        # start a new chat
        if current_conversation["id"] == conversation_id:

            current_conversation = create_conversation()
            messages = current_conversation["messages"]

            # Clear chat window
            for widget in self.chat_frame.winfo_children():
                widget.destroy()

            # Show welcome message
            self.add_message(
                "Hi! I'm Sagar ai running locally on your computer.\n"
                "How can I help you today?",
                sender="bot"
            )

            self.entry.focus_set()

        # Refresh sidebar
        self.refresh_sidebar()



    def refresh_sidebar(self):

        # Remove existing conversation buttons
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        conversations = load_all_conversations()

        for conversation in conversations:

            conversation_frame = ctk.CTkFrame(
                self.history_frame,
                fg_color="transparent"
            )
            conversation_frame.pack(
                fill="x",
                padx=2,
                pady=2
            )

            title = conversation["title"]

            if len(title) > 25:
                title = title[:25] + "..."

            # Conversation title button

            is_active = conversation["id"] == current_conversation["id"]

            if is_active:
                button_color = "#2a2a2a"
                hover_color = "#333333"
            else:
                button_color = "transparent"
                hover_color = "#252525"

                
            button = ctk.CTkButton(
                conversation_frame,
                text=title,
                height=38,
                corner_radius=8,
                fg_color=button_color,
                hover_color=hover_color,
                anchor="w",
                font=("Segoe UI", 11),
                command=lambda cid=conversation["id"]: self.load_chat(cid),
            )

            button.pack(
                side="left",
                fill="x",
                expand=True
            )

            # Delete button
            delete_button = ctk.CTkButton(
                conversation_frame,
                text="×",
                width=30,
                height=38,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#3a2020",
                font=("Segoe UI", 16),
                command=lambda cid=conversation["id"]: self.delete_chat(cid),
            )

            delete_button.pack(
                side="right",
                padx=(2, 0)
            )

    
        # ========================================================

    def add_message(
        self,
        text,
        sender="bot"
    ):

        bubble = ChatBubble(
            self.chat_frame,
            text=text,
            sender=sender
        )

        bubble.pack(
            fill="x",
            anchor="w" if sender == "bot" else "e"
        )

        self.after(
            50,
            self.scroll_to_bottom
        )

        return bubble

    # ========================================================
    # SCROLL
    # ========================================================

    def scroll_to_bottom(self):

        try:

            self.chat_frame._parent_canvas.yview_moveto(
                1.0
            )

        except Exception:
            pass

    # ========================================================
    # SEND MESSAGE
    # ========================================================

    def set_generating_state(self, generating):

        self.generating = generating

        if generating:

            self.entry.configure(
                state="disabled"
            )

            self.send_btn.configure(
                state="disabled",
                text="..."
            )

            self.new_chat_btn.configure(
                state="disabled"
            )

        else:

            self.entry.configure(
                state="normal"
            )

            self.send_btn.configure(
                state="normal",
                text="Send"
            )

            self.new_chat_btn.configure(
                state="normal"
            )



    def send_message(
        self,
        event=None
    ):

        # Don't allow multiple simultaneous requests
        if self.generating:
            return

        user_input = self.entry.get().strip()

        if not user_input:
            return

        # ----------------------------------------------------
        # Clear input
        # ----------------------------------------------------

        self.entry.delete(
            0,
            "end"
        )

        # ----------------------------------------------------
        # Save user message
        # ----------------------------------------------------

        messages.append({
            "role": "user",
            "content": user_input
        })

        save_conversation(current_conversation)

        if current_conversation["title"] == "New Chat":
            current_conversation["title"] = user_input[:40]

            save_conversation(current_conversation)

        # ----------------------------------------------------
        # Display user message
        # ----------------------------------------------------

        self.add_message(
            user_input,
            sender="user"
        )

        # ----------------------------------------------------
        # Lock interface
        # ----------------------------------------------------

        self.set_generating_state(True)


        # ----------------------------------------------------
        # Start background thread
        # ----------------------------------------------------

        thread = threading.Thread(
            target=self.generate_response,
            daemon=True
        )

        thread.start()

    # ========================================================
    # GENERATE RESPONSE
    # ========================================================

    def generate_response(self):

        response = ""
        error = None

        self.after(0, self.start_ai_response)

        try:

            last_update = 0

            for chunk in chat_with_model(messages):

                response += chunk

                current_time = datetime.now().timestamp()

                if current_time - last_update >= 0.04:

                    self.after(
                        0,
                        self.update_ai_response,
                        response
                    )

                    last_update = current_time

            # Make sure the final text is displayed
            self.after(
                0,
                self.update_ai_response,
                response
            )

        except Exception as e:

            error = str(e)

        # Everything after this point is sent
        # back to the main Tkinter thread.

        self.after(
            0,
            self.finish_generation,
            response,
            error
        )


    def finish_generation(self, response, error):

        if error is not None:

            response = (
                "Error communicating with Ollama:\n\n"
                + error
            )

        messages.append({
            "role": "assistant",
            "content": response
        })

        save_conversation(current_conversation)

        self.finish_ai_response()
    # ========================================================
    # START AI RESPONSE
    # ========================================================

    def on_close(self):
        if self.generating:
            confirm = messagebox.askyesno(
                "AI is still generating",
                "The AI is still generating a response.\n\n"
                "Are you sure you want to close the application?"
            )

            if not confirm:
                return

        self.destroy()


    def start_ai_response(self):

        self.current_ai_bubble = ChatBubble(
            self.chat_frame,
            text="",
            sender="bot"
        )

        self.current_ai_bubble.pack(
            fill="x",
            anchor="w"
        )

        self.scroll_to_bottom()

    # ========================================================
    # STREAM AI RESPONSE
    # ========================================================

    def update_ai_response(
        self,
        text
    ):

        if self.current_ai_bubble is None:
            return

        self.current_ai_bubble.update_text(
            text
        )

        self.scroll_to_bottom()

    # ========================================================
    # RESPONSE COMPLETE
    # ========================================================

    def finish_ai_response(self):

        self.current_ai_bubble = None

        self.set_generating_state(False)

        # ----------------------------------------------------
        # Put cursor back automatically
        # ----------------------------------------------------

        self.entry.focus_set()

        self.scroll_to_bottom()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app = ChatbotApp()

    app.mainloop()