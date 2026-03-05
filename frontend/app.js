const { useState } = React;

const App = () => {
  const [movie, setMovie] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = () => {

  if (!movie) return;

  setLoading(true);
  setResults([]);
  setError("");

  fetch(`http://127.0.0.1:5000/recommend?movie=${movie}`)
    .then((response) => response.json())
    .then((data) => {

      setLoading(false);

      if (data.error) {
        setResults([]);
        setError("No results found");
      } else {
        setResults(data.recommendations);
      }

    })
    .catch((error) => {

      console.error(error);
      setLoading(false);
      setResults([]);
      setError("Something went wrong");

    });
};

  return React.createElement(
    "div",
    { className: "container" },

    React.createElement("div", { className: "header" }, "Movie Recommender"),

    error && React.createElement("div", { className: "error-message" }, error),

    React.createElement(
      "div",
      { className: "search-container" },

      React.createElement(
        "div",
        { className: "search-row" },

        React.createElement("input", {
          className: "search-bar",
          placeholder: "Enter movie name...",
          value: movie,
          onChange: (e) => {
            const value = e.target.value;
            setMovie(value);

            if (value.length === 0) {
              setSuggestions([]);
              return;
            }

            fetch(`http://127.0.0.1:5000/search?query=${value}`)
              .then((res) => res.json())
              .then((data) => setSuggestions(data));
          },
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
        { className: "suggestions" },

        suggestions.map((title, index) =>
          React.createElement(
            "div",
            {
              key: index,
              className: "suggestion-item",
              onClick: () => {
                setMovie(title);
                setSuggestions([]);
              },
            },
            title,
          ),
        ),
      ),
    ),

    loading
  ? React.createElement(
      "div",
      { className: "spinner" },
      "Loading recommendations..."
    )
  : React.createElement(
      "div",
      { className: "movies-grid" },

      results.map((movie, index) =>
        React.createElement(
          "div",
          { className: "movie-card", key: index },

          React.createElement("img", {
            src: movie.poster || "https://via.placeholder.com/300x450?text=No+Poster",
            className: "poster",
          }),

          React.createElement("div", { className: "movie-title" }, movie.title),
        )
      )
    )
  );
};

ReactDOM.render(React.createElement(App), document.getElementById("root"));
