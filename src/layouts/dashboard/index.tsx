import { Box } from "@mui/material";
import { Stack } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import Logo from "../../assets/Images/logo.ico";

const DashboardLayout = () => {
    const theme = useTheme();

    console.log(theme);

    return (
        <>
            <Box
                p={2}
                sx={{
                    backgroundColor: theme.palette.background.paper,
                    boxShadow: "0px 0px 2px rgba(0, 0, 0, 0.25)",
                    height: "100vh",
                    width: 100,
                }}
            >
                <Stack direction="column" alignItems={"center"} sx={{width: "100%"}}>
                    <Box
                        sx={{
                            backgroundColor: theme.palette.primary.main,
                            height: 64,
                            width: 64,
                            borderRadius: 1.5,
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                        }}
                    >
                        <img
                            src={Logo}
                            alt="Chat App"
                            style={{ maxWidth: "100%", maxHeight: "100%" }} />
                    </Box>
                </Stack>
            </Box>
        </>
    );
};

export default DashboardLayout;
