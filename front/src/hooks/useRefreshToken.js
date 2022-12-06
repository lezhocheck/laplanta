import axios from "../api/axios";
import useAuth from "./useAuth";

const useRefreshToken = () => {
    const {setAuth} = useAuth();

    const refresh = async () => {
        const respose = await axios.post('/refresh', {
            withCredentials: true
        });
        setAuth(prev => {
            return {...prev, token: respose.data.token};
        });

        return respose.data.token;
    }

    return refresh;
}

export default useRefreshToken;