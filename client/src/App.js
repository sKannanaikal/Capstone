import React, { useState } from 'react' 

function App() {
	const [file, setFile] = useState(null)
	const [model, setModel] = useState('flem_functions_only')
	const [algorithm, setAlgorithm] = useState('LIME')
	
	const submitForm = async (e) => {
		e.preventDefault()

		if(!file){
			alert('Please Choose a File')
			return;
		}

		const formData = new FormData()
		formData.append('sample', file)
		formData.append('model', model)
		formData.append('algorithm', algorithm)

		try {
			const response = await fetch('http://localhost:5000/upload', {
				method: 'POST',
				body: formData
			})

			const result = await response.json()
			console.log('Success: ', result)
		} catch (error) {
			console.log('Error: ', error)
		}
	}

	return (
    	<div>
			<h1 class="text-3xl font-bold underline">FLEM</h1>
			
			<form onSubmit={submitForm} method="POST" enctype="multipart/form-data">
				<input type='file' onChange={(e) => setFile(e.target.files[0])} required ></input>

				<select onChange={(e) => setModel(e.target.value)} id="model" name="model">
					<option value="flem_functions_only">FUNCTIONS_ONLY</option>
					<option value="flem_text_section">EXT_SECTION</option>
					<option value="flem_whole_exe">WHOLE_EXE</option>
					<option value="RAW">RAW</option>
					<option value="DIS">DIS</option>
					<option value="DEC">DEC</option>
				</select>
				
				<select onChange={(e) => setAlgorithm(e.target.value)} id="algorithm" name="algorithm">
					<option value="LIME">LIME</option>
					<option value="SHAP">KERNEL SHAP</option>
				</select>
				
				<input type='submit'></input>
			</form>
    	</div>
  	)
}

export default App