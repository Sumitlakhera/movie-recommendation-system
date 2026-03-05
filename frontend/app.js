const { useState } = React;

const App = () => {
  const [movie, setMovie] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");

  const handleSearch = () => {

    fetch(`http://127.0.0.1:5000/recommend?movie=${movie}`)
    .then(response => response.json())
    .then(data => {

        if (data.error) {

            setResults([]);
            setError("No results found");

        } else {

            setResults(data.recommendations);
            setError("");

        }

    })
    .catch(error => {

        console.error(error);
        setResults([]);
        setError("Something went wrong");

    });

};

  return React.createElement(
    "div",
    { className: "container" },

    React.createElement("div", { className: "header" }, "Movie Recommender"),

    error &&
    React.createElement(
    "div",
    { className: "error-message" },
    error
    ),

    React.createElement(
      "div",
      null,

      React.createElement("input", {
        className: "search-bar",
        placeholder: "Enter movie name...",
        value: movie,
        onChange: (e) => setMovie(e.target.value),
      }),

      React.createElement(
        "button",
        {
          className: "button",
          onClick: handleSearch,
        },
        "Recommend",
      ),
    ),

    React.createElement(
      "div",
      { className: "movies-grid" },

      results.map((movie, index) =>
        React.createElement(
          "div",
          { className: "movie-card", key: index },

          React.createElement("div", { className: "movie-title" }, movie),
        ),
      ),
    ),
  );
};

ReactDOM.render(React.createElement(App), document.getElementById("root"));
