import { createTheme, responsiveFontSizes } from "@mui/material";

let theme = createTheme({
  typography: {
    fontFamily: ["Inter", "sans-serif"].join(","),
  },
  components: {
    MuiAppBar: {
      defaultProps: {
        color: "default",
      },
      styleOverrides: {
        root: {
          boxShadow: "none",
        },
      },
    },
  },
});

theme = responsiveFontSizes(theme);

export { theme };