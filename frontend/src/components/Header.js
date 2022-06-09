import React from 'react'
import { Link } from 'react-router-dom'
import Button from '@mui/material/Button';

/**
 * Haeder del front
 * Menú
 */

export default function Header() {

  return (
    <header class="header header-sticky">
       <h1 class="header-title"> Burbujas 
       Estéticas</h1>
       <Button class="btn" href="#spotify"> Contrarecomendación</Button>
       <Button class="btn" href="#sobre"> Sobre el proyecto</Button>
    </header>
  )
}
