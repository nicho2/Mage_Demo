FROM mageai/mageai:latest

# Download and install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Set the cargo path
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt ${USER_CODE_PATH}/requirements.txt 

RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt
