import {  ReactNode } from "react";

interface contentSectionProps {
    heading: string | null,
    children: ReactNode
}

function ContentSection({heading=null, children}:contentSectionProps ) {

    return (
        <>
            <div className="content-section">
            <h2>{heading}</h2>
                <div>
                {children}
                </div>

            </div>
        </>
    )
} 

export default ContentSection;