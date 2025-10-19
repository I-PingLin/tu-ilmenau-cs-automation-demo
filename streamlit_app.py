import json
import numpy as np
import streamlit as st
from PIL import Image

from modules.ml import train_iris_model, get_iris_data, predict_iris
from modules.cv import preprocess_image, canny_edges
from modules.robotics import generate_grid, a_star, visualize_grid_path
from modules.security import (
    hash_password,
    verify_password,
    generate_jwt,
    decode_jwt,
    generate_fernet_key,
    encrypt_text,
    decrypt_text,
)

st.set_page_config(page_title="CS & Automation Portfolio", page_icon="🤖", layout="wide")


def page_ml():
    st.header("AI/ML: Iris Classification")
    col1, col2, col3 = st.columns(3)
    with col1:
        model_name = st.selectbox("Model", ["Logistic Regression", "Random Forest"])
    with col2:
        test_size = st.slider("Test size", 0.1, 0.5, 0.2, 0.05)
    with col3:
        random_state = st.number_input("Random seed", min_value=0, max_value=9999, value=42, step=1)

    if st.button("Train model"):
        model, metrics = train_iris_model(model_name, test_size, int(random_state))
        st.session_state["ml_model"] = model
        st.session_state["ml_metrics"] = metrics
        st.success(f"Trained {model_name}")

    if "ml_metrics" in st.session_state:
        metrics = st.session_state["ml_metrics"]
        st.metric("Test accuracy", f"{metrics['accuracy']:.3f}")
        st.text(metrics["classification_report"])
        X, y, feature_names, target_names = get_iris_data()
        defaults = X.mean(axis=0)
        with st.form("ml_predict"):
            cols = st.columns(4)
            sepal_length = cols[0].number_input("Sepal length", value=float(defaults[0]), step=0.1, format="%.2f")
            sepal_width  = cols[1].number_input("Sepal width", value=float(defaults[1]), step=0.1, format="%.2f")
            petal_length = cols[2].number_input("Petal length", value=float(defaults[2]), step=0.1, format="%.2f")
            petal_width  = cols[3].number_input("Petal width", value=float(defaults[3]), step=0.1, format="%.2f")
            submitted = st.form_submit_button("Predict")
        if submitted:
            model = st.session_state.get("ml_model")
            if model is None:
                st.warning("Train a model first.")
            else:
                idx, prob_map = predict_iris(
                    model, np.array([sepal_length, sepal_width, petal_length, petal_width])
                )
                label = target_names[idx]
                st.success(f"Prediction: {label}")
                ordered = [prob_map.get(i, 0.0) for i in range(len(target_names))]
                st.bar_chart({name: ordered[i] for i, name in enumerate(target_names)})


def page_cv():
    st.header("Computer Vision: Image Processing and Edges")
    uploaded = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        width = st.slider("Width", 64, 1024, 256, 16)
    with col2:
        height = st.slider("Height", 64, 1024, 256, 16)
    with col3:
        blur = st.select_slider("Blur (kernel)", options=[1, 3, 5, 7], value=3)
    with col4:
        low = st.slider("Canny low", 0, 255, 100, 5)
    high = st.slider("Canny high", 0, 255, 200, 5)

    if uploaded is not None:
        img = Image.open(uploaded)
        proc = preprocess_image(img, width=width, height=height, blur_ksize=blur, grayscale=False)
        edges = canny_edges(
            img, width=width, height=height, blur_ksize=blur, low_threshold=low, high_threshold=high
        )
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Preprocessed")
            st.image(proc, caption=f"{width}x{height}, blur={blur}")
        with c2:
            st.subheader("Edges")
            st.image(edges, clamp=True)


def page_robotics():
    st.header("Robotics: A* Path Planning on a Grid")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        rows = st.slider("Rows", 10, 100, 25, 1)
    with c2:
        cols = st.slider("Cols", 10, 100, 25, 1)
    with c3:
        obstacle_prob = st.slider("Obstacle density", 0.0, 0.6, 0.2, 0.01)
    with c4:
        seed = st.number_input("Seed", min_value=0, max_value=999999, value=42, step=1)

    grid = generate_grid(rows, cols, obstacle_prob=float(obstacle_prob), seed=int(seed))
    st.caption("White=free, Black=obstacle")
    st.image(255 - (grid * 255), clamp=True, width=300)

    c5, c6 = st.columns(2)
    with c5:
        start_r = st.number_input("Start row", 0, rows - 1, 0, 1)
        start_c = st.number_input("Start col", 0, cols - 1, 0, 1)
    with c6:
        goal_r = st.number_input("Goal row", 0, rows - 1, rows - 1, 1)
        goal_c = st.number_input("Goal col", 0, cols - 1, cols - 1, 1)

    start = (int(start_r), int(start_c))
    goal = (int(goal_r), int(goal_c))
    path = a_star(grid, start, goal)
    fig = visualize_grid_path(grid, path, start, goal)
    st.pyplot(fig, use_container_width=True)

    if path:
        st.success(f"Path length: {len(path) - 1} steps")
    else:
        st.error("No path found. Try a lower obstacle density or different start/goal.")


def page_security():
    st.header("Cybersecurity: Hashing, JWT, and Symmetric Encryption")
    tab1, tab2, tab3 = st.tabs(["Password Hashing", "JWT", "Fernet"])

    with tab1:
        pwd = st.text_input("Password to hash", type="password")
        if st.button("Hash password"):
            if not pwd:
                st.warning("Enter a password")
            else:
                st.session_state["hashed_pwd"] = hash_password(pwd)
        hashed_val = st.session_state.get("hashed_pwd", "")
        st.text_area("Hashed (bcrypt)", hashed_val, height=80)
        verify = st.text_input("Verify against hash", type="password", key="verify_pwd")
        if st.button("Check password"):
            if not hashed_val:
                st.warning("Hash a password first.")
            else:
                ok = verify_password(verify, hashed_val)
                st.write("Match" if ok else "No match")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            payload_str = st.text_area("Payload JSON", value='{"user":"alice","role":"researcher"}', height=120)
            secret = st.text_input("Secret key", value="change_me")
            exp = st.slider("Expires (minutes)", 1, 120, 15, 1)
            if st.button("Generate JWT"):
                try:
                    payload = json.loads(payload_str)
                    token = generate_jwt(payload, secret, exp)
                    st.text_area("JWT", token, height=120)
                except Exception as e:
                    st.error(f"Error: {e}")
        with col2:
            token_in = st.text_area("JWT to decode", height=120, key="jwt_in")
            secret_in = st.text_input("Secret for decoding", value="change_me", key="jwt_secret_in")
            if st.button("Decode JWT"):
                try:
                    data = decode_jwt(token_in, secret_in)
                    st.json(data)
                except Exception as e:
                    st.error(f"Decode error: {e}")

    with tab3:
        key = st.text_input("Fernet key (base64, 32-byte)", value=st.session_state.get("fernet_key", ""))
        if st.button("Generate new key"):
            new_key = generate_fernet_key()
            st.session_state["fernet_key"] = new_key
            st.success("Generated new key")
            st.text_input("Fernet key (base64, 32-byte)", value=new_key, key="fernet_key_display")

        plaintext = st.text_area("Plaintext", "Hello TU Ilmenau!")
        if st.button("Encrypt"):
            try:
                if not key:
                    st.warning("Provide a key")
                else:
                    token = encrypt_text(plaintext, key)
                    st.text_area("Ciphertext (token)", token, height=120)
            except Exception as e:
                st.error(f"Encrypt error: {e}")

        token_in = st.text_area("Ciphertext to decrypt", height=120, key="fernet_token_in")
        if st.button("Decrypt"):
            try:
                if not key:
                    st.warning("Provide a key")
                else:
                    text = decrypt_text(token_in, key)
                    st.text_area("Decrypted text", text, height=120)
            except Exception as e:
                st.error(f"Decrypt error: {e}")


def main():
    st.title("Computer Science and Automation — Portfolio Demo")
    st.caption("Ilmenau University of Technology themed demo: AI/ML, CV, Robotics, Cybersecurity")
    choice = st.sidebar.radio("Module", ["AI/ML", "Computer Vision", "Robotics", "Cybersecurity"])
    if choice == "AI/ML":
        page_ml()
    elif choice == "Computer Vision":
        page_cv()
    elif choice == "Robotics":
        page_robotics()
    else:
        page_security()


if __name__ == "__main__":
    main()
