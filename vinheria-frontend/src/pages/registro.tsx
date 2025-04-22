import React, { useRef } from "react"

export const Registro: React.FC = () => {

    //declarar var inputs
    const nameRef = useRef<HTMLInputElement>(null)
    const emailRef = useRef<HTMLInputElement>(null)
    const senhaRef = useRef<HTMLInputElement>(null)

    //pegar os bgls
    const handleRegister = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        const name = nameRef.current?.value
        const email = emailRef.current?.value
        const senha = senhaRef.current?.value
        
        //metodo
        fetch('http://127.0.0.1:3002/api/registro', {
            method: 'POST',
            headers:{
                'Content-Type' : 'application/json',
            },
            body: JSON.stringify({name,email,senha})
        })
    }

    return (

        <div>
            <form onSubmit={handleRegister} className="flex flex-col">
                <input ref={nameRef} name="nome" type="text" placeholder="Nome poha" />
                <input ref={emailRef} name="email" type="text" placeholder="Email" />
                <input ref={senhaRef} name="senha" type="text" placeholder="Senha" />
                <button type="submit">EH DENTO</button>
            </form>
        </div>

    )
}
