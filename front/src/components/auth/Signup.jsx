import Auth from './Auth';
import Button from 'react-bootstrap/Button';
import styles from './Auth.module.scss';
import Form from 'react-bootstrap/Form';
import {FaCheck, FaTimes} from 'react-icons/fa';
import {useRef, useState, useEffect} from 'react';
import axios from '../../api/axios';
import Alert from 'react-bootstrap/Alert';

const EMAIL_REGEX = /^([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])$/;
const USERNAME_REGEX = /^[a-zA-Z0-9._'ЁёА-Яа-я іІґҐїЇЄє]{3,23}$/;
const TELEPHONE_REGEX = /^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/;
const PASSWORD_REGEX = /^[a-zA-Z0-9._-ЁёА-Яа-яіІґҐїЇЄє]{4,24}$/;
const REGISTER_ULR = '/user/signup';

const Signup = () => {
    const emailRef = useRef();

    const [email, setEmail] = useState('');
    const [validEmail, setValidEmail] = useState(false);
    const [emailFocus, setEmailFocus] = useState(false);

    const [username, setUsername] = useState('');
    const [validUsername, setValidUsername] = useState(false);
    const [usernameFocus, setUsernameFocus] = useState(false);

    const [telephone, setTelephone] = useState('');
    const [validTelephone, setValidTelephone] = useState(false);
    const [telephoneFocus, setTelephoneFocus] = useState(false);

    const [password, setPassword] = useState('');
    const [validPassword, setValidPassword] = useState(false);
    const [passwordFocus, setPasswordFocus] = useState(false);

    const [matchingPassword, setMatchingPassword] = useState('');
    const [validMatchingPassword, setValidMatchingPassword] = useState(false);
    const [matchingPasswordFocus, setMatchingPasswordFocus] = useState(false);

    const [errorMessage, setErrorMessage] = useState('');
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        emailRef.current.focus();
    }, []);

    useEffect(() => {
        const result = EMAIL_REGEX.test(email);
        setValidEmail(result);
    }, [email]);

    useEffect(() => {
        const result = USERNAME_REGEX.test(username);
        setValidUsername(result);
    }, [username]);

    useEffect(() => {
        const result = TELEPHONE_REGEX.test(telephone);
        setValidTelephone(result);
    }, [telephone]);

    useEffect(() => {
        const result = PASSWORD_REGEX.test(password);
        setValidPassword(result);
        const match = password === matchingPassword;
        setValidMatchingPassword(match);
    }, [password, matchingPassword]);

    useEffect(() => {
        setErrorMessage('');
    }, [email, username, telephone, password, matchingPassword]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const v1 = EMAIL_REGEX.test(email);
        const v2 = USERNAME_REGEX.test(username);
        const v3 = TELEPHONE_REGEX.test(telephone);
        const v4 = PASSWORD_REGEX.test(password);
        if (!v1 || !v2 || !v3 || !v4) {
            setErrorMessage('Invalid input');
            return;
        }

        try {
            const response = await axios.post(REGISTER_ULR, 
                JSON.stringify({name: username, email, password, telephone}),
                {
                    headers: {'Content-Type': 'application/json'}
                }
            );
            setSuccess(true);
            setEmail('');
            setUsername('');
            setTelephone('');
            setPassword('');
            setMatchingPassword('');
        } catch(e) {
            if (!e?.response) {
                setErrorMessage("Cannot signup now");
            } else {
                var message = e.response.data?.message;
                setErrorMessage(message);
            }
        }
    };

    return (
        <Auth subtitle="Create new account">
            <Alert key="danger" variant="danger" aria-live="assertive"
                className={errorMessage ? "d-block" : "d-none"}>
                {errorMessage}
            </Alert>
            <Form onSubmit={handleSubmit} className={styles.input}>
                <Form.Group>
                    <Form.Label htmlFor="signup-username">
                        Username&nbsp;
                        <span className={validUsername ? "": "d-none"}>
                            <FaCheck color='green' size={16}/>
                        </span>
                        <span className={validUsername || !username ? "d-none": ""}>
                            <FaTimes color='red' size={16}/>
                        </span>
                    </Form.Label>
                    <Form.Control 
                        type="text" 
                        id="signup-username" 
                        placeholder="Enter your name" 
                        aria-describedby="signup-username-helper"
                        required
                        onChange={(e) => setUsername(e.target.value)}
                        aria-invalid={validUsername ? "false" : "true"}
                        onFocus={() => setUsernameFocus(true)}
                        onBlur={() => setUsernameFocus(false)}
                    />
                    <Form.Text id="signup-username-helper"
                        className={usernameFocus && username && !validUsername ? "d-block" : "d-none"}>
                        Must contain alpanumeric symbols (3-23), i.e.: John Doe
                    </Form.Text>
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="signup-email">
                        Email&nbsp;
                        <span className={validEmail ? "": "d-none"}>
                            <FaCheck color='green' size={16}/>
                        </span>
                        <span className={validEmail || !email ? "d-none": ""}>
                            <FaTimes color='red' size={16}/>
                        </span>
                    </Form.Label>
                    <Form.Control 
                        type="text" 
                        id="signup-email" 
                        placeholder="Enter your email" 
                        ref={emailRef}
                        aria-describedby="signup-email-helper"
                        required
                        onChange={(e) => setEmail(e.target.value)}
                        aria-invalid={validEmail ? "false" : "true"}
                        onFocus={() => setEmailFocus(true)}
                        onBlur={() => setEmailFocus(false)}
                    />
                    <Form.Text id="signup-email-helper"
                        className={emailFocus && email && !validEmail ? "d-block" : "d-none"}>
                        Must be a valid email address, i.e.: john-doe@example.com
                    </Form.Text>
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="signup-telephone">
                        Telephone&nbsp;
                        <span className={validTelephone ? "": "d-none"}>
                            <FaCheck color='green' size={16}/>
                        </span>
                        <span className={validTelephone || !telephone ? "d-none": ""}>
                            <FaTimes color='red' size={16}/>
                        </span>
                    </Form.Label>
                    <Form.Control 
                        type="tell" 
                        id="signup-telephone" 
                        placeholder="Enter your telephone number" 
                        aria-describedby="signup-telephone-helper"
                        required
                        onChange={(e) => setTelephone(e.target.value)}
                        aria-invalid={validTelephone ? "false" : "true"}
                        onFocus={() => setTelephoneFocus(true)}
                        onBlur={() => setTelephoneFocus(false)}
                    />
                    <Form.Text id="signup-telephone-helper"
                        className={telephoneFocus && telephone && !validTelephone ? "d-block" : "d-none"}>
                        Must be a valid telephone number, i.e.: +380684552323
                    </Form.Text>
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="signup-password">
                        Password&nbsp;
                        <span className={validPassword ? "": "d-none"}>
                            <FaCheck color='green' size={16}/>
                        </span>
                        <span className={validPassword || !password ? "d-none": ""}>
                            <FaTimes color='red' size={16}/>
                        </span>
                    </Form.Label>
                    <Form.Control 
                        type="password" 
                        id="signup-password" 
                        placeholder="Come up with your password" 
                        aria-describedby="signup-password-helper"
                        required
                        onChange={(e) => setPassword(e.target.value)}
                        aria-invalid={validPassword ? "false" : "true"}
                        onFocus={() => setPasswordFocus(true)}
                        onBlur={() => setPasswordFocus(false)}
                    />
                    <Form.Text id="signup-password-helper"
                        className={passwordFocus && password && !validPassword ? "d-block" : "d-none"}>
                        Must contain alpanumeric symbols (4-24)
                    </Form.Text>
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="signup-matching-password">
                        Confirm password&nbsp;
                        <span className={validMatchingPassword && matchingPassword ? "": "d-none"}>
                            <FaCheck color='green' size={16}/>
                        </span>
                        <span className={validMatchingPassword || !matchingPassword ? "d-none": ""}>
                            <FaTimes color='red' size={16}/>
                        </span>
                    </Form.Label>
                    <Form.Control 
                        type="password" 
                        id="signup-matching-password" 
                        placeholder="Enter your password one more time" 
                        aria-describedby="signup-matching-password-helper"
                        required
                        onChange={(e) => setMatchingPassword(e.target.value)}
                        aria-invalid={validMatchingPassword ? "false" : "true"}
                        onFocus={() => setMatchingPasswordFocus(true)}
                        onBlur={() => setMatchingPasswordFocus(false)}
                    />
                    <Form.Text id="signup-matching-password-helper"
                        className={matchingPasswordFocus && !validMatchingPassword ? "d-block" : "d-none"}>
                        Passwords must match
                    </Form.Text>
                </Form.Group>
            <div className={styles.login}>
                <Button variant="dark" type="submit" disabled={!validEmail || !validUsername
                     || !validTelephone || !validPassword || !validMatchingPassword ? true : false} style={{width: '30%'}}>Signup</Button>
                <p className="mb-5 pb-lg-2 text-dark">Already have an account? <a href="#!">Login here</a></p>
            </div>    
            </Form>
        </Auth>
    );
}

export default Signup;