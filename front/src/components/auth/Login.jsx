import Auth from './Auth';
import Button from 'react-bootstrap/Button';
import styles from './Auth.module.scss';
import Form from 'react-bootstrap/Form';
import {useRef, useState, useEffect} from 'react';
import useAuth from '../../hooks/useAuth';
import axios from '../../api/axios';
import {useNavigate, useLocation} from 'react-router-dom';
import Alert from 'react-bootstrap/Alert';
import {Link} from 'react-router-dom';
import {useTranslation} from 'react-i18next';

const LOGIN_ULR = '/user/login';

const Login = () => {
    const {t} = useTranslation();
    const {setAuth} = useAuth();

    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname || "/";

    const emailRef = useRef();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
       emailRef.current.focus(); 
    }, []);

    useEffect(() => {
        setErrorMessage('');
    }, [email, password]);

    const handleSubmit = async(e) => {
        e.preventDefault();
        try {
            const response = await axios.post(LOGIN_ULR,
                JSON.stringify({email, password}), 
                {
                    headers: {'Content-Type': 'application/json',
                        withCredentials: true
                    }
                }
            );
            const accessToken = response?.data?.msg?.token;
            setAuth({email, password, accessToken});
            setEmail('');
            setPassword('');
            navigate(from, {replace: true});
        } catch(e) {
            if (!e?.response) {
                setErrorMessage("Cannot login. Please try again");
            } else {
                var message = e.response.data?.msg;
                setErrorMessage(message);
            }
        }
    }
 
    return (
        <Auth subtitle={t("login_message")}>
            <Alert key="danger" variant="danger" aria-live="assertive"
                className={errorMessage ? "d-block" : "d-none"}>
                {errorMessage}
            </Alert>
            <Form onSubmit={handleSubmit} className={styles.input}>
                <Form.Group>
                    <Form.Label htmlFor="login-email">{t("email")}</Form.Label>
                    <Form.Control 
                        type="text" 
                        id="login-email" 
                        placeholder={t("enter_your_email")}
                        ref={emailRef}
                        aria-describedby="login-email-helper"
                        required
                        onChange={(e) => setEmail(e.target.value)}
                        value={email}
                    />
                    <Form.Text id="login-email-helper" muted>
                        {t("login_help")}
                    </Form.Text>
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="login-password">{t("password")}</Form.Label>
                    <Form.Control 
                        type="password" 
                        id="login-password" 
                        placeholder={t("enter_your_password")}
                        aria-describedby="login-password-helper"
                        required
                        onChange={(e) => setPassword(e.target.value)}
                        value={password}
                    />
                    <Form.Text id="login-password-helper" muted>
                        {t("password_help")}
                    </Form.Text>
                </Form.Group>
                <div className={styles.login}>
                    <Button variant="dark" type="submit" style={{width: '30%'}}>{t("login")}</Button>
                    <p className="mb-5 pb-lg-2 text-dark">{t("no_account") + ' '} <Link to="/signup">{t("register_here")}</Link></p>
                </div>
            </Form>   
        </Auth>
    );
}

export default Login;