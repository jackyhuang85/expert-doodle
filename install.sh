main() {
    PWD="$(pwd)"
    
    # Check conda environment available
    if ! conda --version; then
        echo 'Conda is not installed! Please install conda first!\n'
        exit
    fi
    
    # Check pip environment
    if ! pip --version; then
        echo 'Pip is not installed! Please install pip first!\n'
        exit
    fi

    conda install opencv
    conda install -c conda-forge pyopencl

    pip install gputools

    # Check git environment
    if ! git --version; then
        echo 'Git is not installed! Please install git first!\n'
        exit
    fi

    git clone https://github.com/jackyhuang85/expert-doodle.git
    cd ${PWD}/expert-doodle/ 

    echo 'Expert-doodle is now installed.'
    echo ''
    echo 'Please enter: python src/main.py'
    echo 'to get started!'
    echo ''
    echo 'p.s. Good luck!'
}

main
