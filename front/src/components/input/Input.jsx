import Form from 'react-bootstrap/Form';

const Input = (props) => {
    const label = props.label;
    const type = props.type;
    const placeholder = props.placeholder;
    const description = props.description;
    const id = props.id;
    const idHelp = id + '-help';

    return (
        <Form.Group>
            <Form.Label htmlFor={id}>{label}</Form.Label>
            <Form.Control type={type} id={id} placeholder={placeholder} aria-describedby={idHelp}/>
            <Form.Text id={idHelp} muted>
                {description}
            </Form.Text>
        </Form.Group>
    );
}

export default Input;