const { useState } = React;

const App = () => {

    const [movie, setMovie] = useState("");
    const [results, setResults] = useState([]);

    const handleSearch = () => {

        console.log("Search movie:", movie);

        // placeholder results
        setResults([
            "Example Movie 1",
            "Example Movie 2",
            "Example Movie 3"
        ]);

    };

    return (

        React.createElement(
            "div",
            { className: "container" },

            React.createElement(
                "div",
                { className: "header" },
                "Movie Recommender"
            ),

            React.createElement(
                "div",
                null,

                React.createElement(
                    "input",
                    {
                        className: "search-bar",
                        placeholder: "Enter movie name...",
                        value: movie,
                        onChange: (e) => setMovie(e.target.value)
                    }
                ),

                React.createElement(
                    "button",
                    {
                        className: "button",
                        onClick: handleSearch
                    },
                    "Recommend"
                )
            ),

            React.createElement(
                "div",
                { className: "movies-grid" },

                results.map((movie, index) =>
                    React.createElement(
                        "div",
                        { className: "movie-card", key: index },

                        React.createElement(
                            "div",
                            { className: "movie-title" },
                            movie
                        )
                    )
                )
            )

        )

    );

};

ReactDOM.render(
    React.createElement(App),
    document.getElementById("root")
);