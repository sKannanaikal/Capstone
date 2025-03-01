#base build not sure if to do this, python image, or a base ubuntu image
FROM ubuntu:latest

WORKDIR /server

#install conda
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define Conda installation directory
ENV CONDA_DIR=/opt/conda

# Download and install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p $CONDA_DIR \
    && rm /tmp/miniconda.sh

# Add Conda to the system PATH
ENV PATH="$CONDA_DIR/bin:$PATH"

# Verify installation
RUN conda --version

#install all conda dependencies and start up virtual environment
COPY ./environment.yml .

RUN conda env create -f environment.yml

#install ghidra and copy in ghidra scripts
RUN apt-get update && apt-get install -y \
    openjdk-21-jdk \
    unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget -q https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.0_build/ghidra_11.0_PUBLIC_20231222.zip && \
    unzip ghidra_11.0_PUBLIC_20231222.zip && \
    rm ghidra_11.0_PUBLIC_20231222.zip

ENV GHIDRA_HOME=/server/ghidra_11.0_PUBLIC

RUN mkdir ./ghidra_11.0_PUBLIC/ghidra_scripts

COPY ./ghidraScripts/*  ./ghidra_11.0_PUBLIC/ghidra_scripts/

#move all code and files into container and install flask
COPY ./models/* ./models/
COPY ./*.py .
RUN mkdir disassembled
RUN mkdir uploads


#start up flask server
EXPOSE 5000
CMD ["conda", "activate", "flem", "&&", "python3", "app.py"]
