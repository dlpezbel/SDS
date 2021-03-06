import uuid


class Make_dockerfile:

    def write_docker_file_from_dynamic(container, dockerfile_fixes):
        image = container.image
        f = open('output/Dockerfile', mode='wt', encoding='utf-8')
        f.write("FROM " + str(image.attrs.get('RepoTags')[0]) + "\n\n")
        [f.write(o['content']) for o in dockerfile_fixes]
        f.close()

    def write_docker_file_from_static(instructions, dockerfile_fixes):
        f = open('output/Dockerfile', mode='wt', encoding='utf-8')
        proposed_dockerfile_instructions = Make_dockerfile.generate_proposed_dockerfile(instructions, dockerfile_fixes)
        [f.write(o['content']) for o in proposed_dockerfile_instructions]
        f.close()
        return proposed_dockerfile_instructions

    def generate_proposed_dockerfile(instructions, dockerfile_fixes):
        proposed_dockerfile_instructions = []
        for instruction in instructions:
            if instruction['startline'] in Make_dockerfile.get_lines_with_fixes(dockerfile_fixes):
                next(proposed_dockerfile_instructions.append(o) for o in dockerfile_fixes
                     if 'startline' in o and o['startline'] == instruction['startline'])
            else:
                proposed_dockerfile_instructions.append(instruction)
        [proposed_dockerfile_instructions.append(o) for o in dockerfile_fixes if 'startline' not in o]
        return proposed_dockerfile_instructions

    def get_lines_with_fixes(dockerfile_fixes):
        return list(x['startline'] for x in dockerfile_fixes if 'startline' in x)


def write_dockerfile(dockerfile):
    filename = uuid.uuid4()
    temp_file = open("output/" + str(filename), "w")
    temp_file.write(dockerfile)
    temp_file.close()
    return "output/" + str(filename)
